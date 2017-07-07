import hashlib
import re
from django.db import models
from django.utils.crypto import get_random_string

from base.error import Error
from base.response import Ret


class User(models.Model):
    """
    用户类
    """

    TYPE_BUYER = 0
    TYPE_SELLER = 1
    TYPE_TABLE = (
        (TYPE_BUYER, '买家'),
        (TYPE_SELLER, '卖家'),
    )

    L = {
        'user_id': 32,
        'username': 20,
        'password': 32,
        'real_name': 64,
        'address': 512,
        'brand': 32,
    }

    user_id = models.CharField(
        verbose_name='用户ID',
        max_length=L['user_id'],
        primary_key=True,
    )
    user_type = models.IntegerField(
        verbose_name='用户类型',
        help_text='买家和卖家',
        choices=TYPE_TABLE,
    )
    username = models.CharField(
        verbose_name='用户名',
        max_length=L['username'],
        unique=True,
    )
    password = models.CharField(
        verbose_name='MD5密码',
        max_length=L['password'],
    )
    real_name = models.CharField(
        verbose_name='真实姓名',
        max_length=L['real_name'],
        default=None,
        null=True,
        blank=True,
    )
    address = models.CharField(
        verbose_name='住址或仓库地址',
        max_length=L['address'],
        default=None,
        null=True,
        blank=True,
    )
    brand = models.CharField(
        verbose_name='卖家商家品牌',
        max_length=L['brand'],
    )
    default_card = models.ForeignKey(
        'Card.Card',
        verbose_name='默认银行卡',
        default=None,
        null=True,
        blank=True,
    )

    @staticmethod
    def get_md5(raw_pwd):
        md5 = hashlib.md5()
        md5.update(raw_pwd.encode())
        return md5.hexdigest()

    @classmethod
    def create(cls, username, raw_pwd, user_type, brand=''):
        """
        创建用户
        :param brand: 商家品牌（user_type=User.TYPE_SELLER时有效）
        :param user_type: 用户类型 只能是TYPE_TABLE内的值
        :param username: 用户名
        :param raw_pwd: 未加密密码
        :return: 创建成功返回用户类，不成功返回错误代码
        """
        if not len(raw_pwd) >= 6:
            return Ret(Error.PASSWORD_LENGTH)
        if user_type == User.TYPE_SELLER:
            if not User.L['brand'] >= len(brand) >= 2:
                return Ret(Error.BRAND_LENGTH)
            if not User.L['username'] >= len(username) >= 4:
                return Ret(Error.USERNAME_LENGTH)
        else:
            phone_regex = '^1[34578]\d{9}$'
            if re.search(phone_regex, username) is None:
                return Ret(Error.PHONE_FORMAT)
        password = User.get_md5(raw_pwd)
        user_id = User.get_md5(username+get_random_string(length=8))
        try:
            cls.objects.get(username=username)
            return Ret(Error.EXIST_USERNAME)
        except:
            pass
        o = cls(
            user_id=user_id,
            user_type=user_type,
            username=username,
            password=password,
            brand=brand,
        )
        try:
            o.save()
            return Ret(Error.OK, o)
        except:
            return Ret(Error.ERROR_USER_CREATE)

    @staticmethod
    def get(user_id):
        """
        根据用户ID获取用户类
        :param user_id: 用户ID
        :return: 用户类
        """
        try:
            o = User.objects.get(pk=user_id)
        except:
            return Ret(Error.NOT_FOUND_USER)
        return Ret(Error.OK, o)

    @staticmethod
    def check_password(username, raw_pwd):
        """
        登录
        :param username: 用户名
        :param raw_pwd: 密码
        :return: 用户名密码匹配返回用户类，不成功返回错误代码
        """
        try:
            o = User.objects.get(username=username)
        except:
            return Ret(Error.NOT_FOUND_USERNAME)
        if o.password != User.get_md5(raw_pwd):
            return Ret(Error.ERROR_PASSWORD)
        return Ret(Error.OK, o)

    def edit_info(self, address, real_name):
        """
        编辑信息
        :param address: 地址
        :param real_name: 真实姓名
        """
        if self.user_type != User.TYPE_BUYER:
            return Ret(Error.REQUIRE_BUYER)
        if User.L['address'] < len(address):
            return Ret(Error.ADDRESS_LENGTH)
        if User.L['real_name'] < len(real_name):
            return Ret(Error.REAL_NAME_LENGTH)
        self.address = address
        self.real_name = real_name
        self.save()
        return Ret()

    def get_info(self):
        """
        获取信息
        :return: 地址 真实姓名
        """
        if self.user_type != User.TYPE_BUYER:
            return Ret(Error.REQUIRE_BUYER)
        return Ret(Error.OK, dict(address=self.address, real_name=self.real_name))

    def get_card_list(self):
        """
        获取用户银行卡列表
        :return: 银行卡列表
        """
        from Card.models import Card
        cards = Card.objects.filter(owner=self)
        card_list = []
        for o_card in cards:
            card_list.append(dict(
                card_id=o_card.pk,
                card=o_card.card,
                is_default=o_card == self.default_card
            ))
        return Ret(Error.OK, card_list)

    def get_good_list(self):
        """
        获取商家商品列表
        :return: 商品列表
        """
        if self.user_type != User.TYPE_SELLER:
            return Ret(Error.REQUIRE_SELLER)

        from Good.models import Good
        goods = Good.objects.filter(seller=self, is_deleted=False)
        good_list = []
        for o_good in goods:
            good_list.append(dict(
                good_id=o_good.pk,
                brand=o_good.seller.brand,
                good_name=o_good.good_name,
                store=o_good.store,
                price=o_good.price,
                pic=o_good.get_pic(),
            ))
        return Ret(Error.OK, good_list)

    def get_button_list(self):
        """
        获取买家设置列表
        :return: 设置列表
        """
        if self.user_type != User.TYPE_BUYER:
            return Ret(Error.REQUIRE_BUYER)

        from Good.models import Button
        buttons = Button.objects.filter(owner=self)
        button_list = []
        for button in buttons:
            button_list.append(dict(
                button_id=button.pk,
                category_id=button.category_id,
                category_name=button.category.category_name,
                good_id=button.default_good_id,
                good_name=button.default_good.good_name,
                number=button.buy_num,
            ))
        return Ret(Error.OK, button_list)

    def get_order_list(self, order_status, page, count):
        """
        获取订单列表
        :param order_status: 订单筛选
        :param page: 返回结果的第几页
        :param count: 每页显示条数
        :return: 订单列表及是否到达末尾
        """
        try:
            page = int(page)
            assert page >= 0
        except:
            return Ret(Error.ERROR_PAGE)  # 错误的页码
        try:
            count = int(count)
            assert count >= 0
        except:
            return Ret(Error.ERROR_COUNT)  # 错误的条数

        from Order.models import Order
        if self.user_type == User.TYPE_BUYER:
            orders = Order.objects.filter(buyer=self, status=order_status).order_by('-pk')
        else:
            orders = Order.objects.filter(good__seller=self, status=order_status).order_by('-pk')
        is_over = len(orders) <= (page+1) * count
        orders = orders[page*count: (page+1)*count]
        order_list = []
        for o_order in orders:
            order_list.append(dict(
                order_id=o_order.pk,
                good_name=o_order.good_name,
                real_name=o_order.real_name,
                phone=o_order.buyer.username,
                address=o_order.address,
                number=o_order.buy_num,
                price=o_order.price,
                pic=o_order.good.pic,
            ))
        return Ret(Error.OK, dict(order_list=order_list, is_over=is_over))
