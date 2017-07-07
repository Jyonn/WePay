import datetime
from django.db import models

from Good.models import Good, Button
from User.models import User
from base.error import Error
from base.response import Ret


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
            return Ret(Error.REQUIRE_BUYER)

        try:
            o_button = Button.objects.get(owner=o_user, category=o_category)
        except:
            return Ret(Error.REQUIRE_SET_BUTTON)
        if None in [o_user.address, o_user.real_name]:  # 未完善收货信息
            return Ret(Error.REQUIRE_COMPLETE_BUYER_INFO)
        if o_button.default_good.is_deleted:  # 商品被删除（下架）
            return Ret(Error.DELETED_GOOD)
        if o_user.default_card is None:  # 未设置默认银行卡
            return Ret(Error.REQUIRE_ADD_DEFAULT_CARD)
        if o_button.buy_num > o_button.default_good.store:  # 库存不足
            return Ret(Error.LACK_STORE)

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
            return Ret(Error.ERROR_ORDER_CREATE)

        o_button.default_good.store -= o_button.buy_num
        o_button.default_good.save()
        return Ret(Error.OK, o)

    @staticmethod
    def get(order_id):
        """
        根据订单ID获取订单类
        :param order_id: 订单ID
        :return: 订单类
        """
        try:
            o = Order.objects.get(pk=order_id)
        except:
            return Ret(Error.NOT_FOUND_ORDER)
        return Ret(Error.OK, o)

    def confirm_send(self, o_user):
        """
        商家确认发货
        :param o_user: 商家用户类
        """
        if self.good.seller != o_user:
            return Ret(Error.NOT_YOUR_GOOD)
        if self.status != Order.STATUS_CONFIRM_ORDER_BY_SELLER:
            return Ret(Error.ERROR_ORDER_STATUS)
        self.status = Order.STATUS_CONFIRM_DELIVER
        self.deliver_time = datetime.datetime.now()
        self.save()
        return Ret(Error.OK)

    def confirm_receive(self, o_user):
        """
        买家确认收货
        :param o_user: 买家用户类
        """
        if self.buyer != o_user:
            return Ret(Error.NOT_FOUND_GOOD)
        if self.status != Order.STATUS_CONFIRM_DELIVER:
            return Ret(Error.ERROR_ORDER_STATUS)
        self.status = Order.STATUS_CONFIRM_RECEIVE
        self.save()
        return Ret(Error.OK)
