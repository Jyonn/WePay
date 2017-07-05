from django.db import models

from Good.models import Good, Button
from User.models import User
from base.error import Error
from base.response import ret


class Order(models.Model):
    """
    订单类
    """

    STATUS_CONFIRM_ORDER_BY_SELLER = 5
    STATUS_CONFIRM_DELIVER = 6
    STATUS_CONFIRM_RECEIVE = 7

    STATUS_TABLE = (
        (STATUS_CONFIRM_ORDER_BY_SELLER, '确认接单'),
        (STATUS_CONFIRM_DELIVER, '确认发货'),
        (STATUS_CONFIRM_RECEIVE, '确认收货'),
    )

    L = {
        'address': 512,
        'real_name': 64,
        'good_name': 20,
    }

    buyer = models.ForeignKey(
        User,
        verbose_name='买家',
        db_index=True,
    )
    real_name = models.CharField(
        verbose_name='买家姓名',
        max_length=L['real_name'],
    )
    address = models.CharField(
        verbose_name='买家地址',
        max_length=L['address'],
    )
    good = models.ForeignKey(
        Good,
        verbose_name='商品',
    )
    good_name = models.CharField(
        verbose_name='商品名称',
        max_length=L['good_name'],
    )
    buy_num = models.IntegerField(
        verbose_name='购买数量',
        default=0,
    )
    price = models.FloatField(
        verbose_name='购买时单价',
        default=0,
    )
    create_time = models.DateTimeField(
        verbose_name='创建时间',
        auto_created=True,
        auto_now=True,
    )
    deliver_time = models.DateTimeField(
        verbose_name='发货时间',
        default=None,
        null=True,
        blank=True,
    )
    status = models.IntegerField(
        verbose_name='订单状态',
        choices=STATUS_TABLE,
        default=STATUS_CONFIRM_ORDER_BY_SELLER,
    )

    @classmethod
    def create(cls, o_user, o_category):
        """
        创建订单类
        :param o_user: 买家用户类
        :param o_category: 商品类别
        :return: 创建成功则返回订单类，否则返回错误代码
        """
        if o_user.user_type == User.TYPE_SELLER:
            return ret(Error.REQUIRE_BUYER)

        try:
            o_button = Button.objects.get(owner=o_user, category=o_category)
        except:
            return ret(Error.REQUIRE_SET_BUTTON)
        if None in [o_user.address, o_user.real_name]:  # 未完善收货信息
            return ret(Error.REQUIRE_COMPLETE_BUYER_INFO)
        if o_button.default_good.is_deleted:  # 商品被删除（下架）
            return ret(Error.DELETED_GOOD)
        if o_user.default_card is None:  # 未设置默认银行卡
            return ret(Error.REQUIRE_ADD_DEFAULT_CARD)
        if o_button.buy_num > o_button.default_good.store:  # 库存不足
            return ret(Error.LACK_STORE)

        o = cls(
            buyer=o_user,
            address=o_user.address,
            good=o_button.default_good,
            good_name=o_button.default_good.good_name,
            buy_num=o_button.buy_num,
            price=o_button.default_good.price * o_button.buy_num,
            status=Order.STATUS_CONFIRM_ORDER_BY_SELLER,
        )
        try:
            o.save()
        except:
            return ret(Error.ERROR_ORDER_CREATE)

        o_button.default_good.store -= o_button.buy_num
        o_button.default_good.save()
        return ret(Error.OK, o)

    @staticmethod
    def get_list(o_user, order_status, page):
        """
        获取订单列表
        :param o_user: 用户类
        :param order_status: 订单筛选
        :param page: 返回结果的第几页
        :return: 订单列表及是否到达末尾
        """
        try:
            page = int(page)
            assert page >= 0
        except:
            return ret(Error.ERROR_PAGE)
        if o_user.user_type == User.TYPE_BUYER:
            orders = Order.objects.filter(buyer=o_user, status=order_status).order_by('-pk')
        else:
            orders = Order.objects.filter(good__seller=o_user, status=order_status).order_by('-pk')
        is_over = len(orders) <= (page+1) * 10
        orders = orders[page*10: (page+1)*10]
        order_list = []
        for o_order in orders:
            order_list.append(dict(
                order_id=o_order.pk,
                good_name=o_order.good_name,
                real_name=o_order.real_name,
                phone=o_order.buyer.username,
                address=o_order.address,
                number=o_order.buy_num,
            ))
        return ret(Error.OK, dict(order_list=order_list, is_over=is_over))

    def confirm_send(self, o_user):
        """
        商家确认发货
        :param o_user: 商家用户类
        """
        if self.good.seller != o_user:
            return ret(Error.NOT_YOUR_GOOD)
        if self.status != Order.STATUS_CONFIRM_ORDER_BY_SELLER:
            return ret(Error.ERROR_ORDER_STATUS)
        self.status = Order.STATUS_CONFIRM_DELIVER
        return ret(Error.OK)

    def confirm_receive(self, o_user):
        """
        买家确认收货
        :param o_user: 买家用户类
        """
        if self.buyer != o_user:
            return ret(Error.NOT_FOUND_GOOD)
        if self.status != Order.STATUS_CONFIRM_DELIVER:
            return ret(Error.ERROR_ORDER_STATUS)
        self.status = Order.STATUS_CONFIRM_RECEIVE
        return ret(Error.OK)
