import hashlib
import re
from django.db import models
from django.utils.crypto import get_random_string

from base.error import Error
from base.response import ret


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

    @staticmethod
    def get_md5(raw_pwd):
        md5 = hashlib.md5()
        md5.update(raw_pwd.encode())
        return md5.hexdigest()

    @classmethod
    def create(cls, username, raw_pwd, user_type, brand):
        """
        创建用户
        :param brand: 商家品牌（user_type=User.TYPE_SELLER时有效）
        :param user_type: 用户类型 只能是TYPE_TABLE内的值
        :param username: 用户名
        :param raw_pwd: 未加密密码
        :return: 创建成功返回用户类，不成功返回错误代码
        """
        if user_type == User.TYPE_SELLER:
            if not User.L['brand'] > len(brand) > 2:
                return ret(Error.BRAND_LENGTH)
            if not User.L['username'] > len(username) > 4:
                return ret(Error.USERNAME_LENGTH)
        else:
            phone_regex = '^1[3458]\d{9}$'
            if re.search(phone_regex, username) is None:
                return ret(Error.PHONE_FORMAT)
        password = User.get_md5(raw_pwd)
        user_id = User.get_md5(username+get_random_string(length=8))
        try:
            cls.objects.get(username=username)
            return ret(Error.EXIST_USERNAME)
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
            return ret(Error.OK, o)
        except:
            return ret(Error.ERROR_USER_CREATE)

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
            return ret(Error.NOT_FOUND_USERNAME)
        if o.password != User.get_md5(raw_pwd):
            return ret(Error.ERROR_PASSWORD)
        return ret(Error.OK, o)
