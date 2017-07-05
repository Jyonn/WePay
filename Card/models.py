from django.db import models

from User.models import User
from base.error import Error
from base.response import ret


class Card(models.Model):
    L = {
        'card': 20,
    }
    owner = models.ForeignKey(
        'User.User',
        verbose_name='关联用户',
        db_index=True,
    )
    card = models.CharField(
        verbose_name='银行卡号',
        max_length=L['card'],
        unique=True,
    )

    @classmethod
    def create(cls, o_user, card, is_default):
        """
        新增银行卡
        :param o_user: 用户
        :param card: 银行卡号
        :param is_default: 是否设为默认
        :return:
        """
        if o_user.user_type != User.TYPE_BUYER:
            return ret(Error.REQUIRE_BUYER)

        o = cls(user=o_user, card=card)
        try:
            o.save()
        except:
            return ret(Error.ERROR_CARD_CREATE)
        if is_default:
            o.owner.default_card = o
            o.owner.save()
        return ret(Error.OK, o)

    def set_default(self, o_user):
        """
        设为默认银行卡
        """
        if self.owner != o_user:
            return ret(Error.NOT_YOUR_CARD)
        self.owner.default_card = self
        self.owner.save()
        return ret()

    def safe_delete(self, o_user):
        """
        安全删除银行卡
        """
        if self.owner != o_user:
            return ret(Error.NOT_YOUR_CARD)
        if self.owner.default_card == self:
            self.owner.default_card = None
            self.owner.save()
        self.delete()
        return ret()
