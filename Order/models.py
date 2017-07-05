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
        'good_name': 20,
    }

    buyer = models.ForeignKey(
        User,
        verbose_name='买家',
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
