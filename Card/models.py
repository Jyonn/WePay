from django.db import models

from User.models import User
from base.error import Error
from base.response import Ret


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
        o = cls(user=o_user, card=card)
        try:
            o.save()
        except:
            return Ret(Error.ERROR_CARD_CREATE)
        if is_default:
            o.owner.default_card = o
            o.owner.save()
        return Ret(Error.OK, o)

    @staticmethod
    def get(card_id):
        """
        根据银行卡ID获取银行卡类
        :param card_id: 银行卡ID
        :return: 银行卡类
        """
        try:
            o = Card.objects.get(pk=card_id)
        except:
            return Ret(Error.NOT_FOUND_CARD)
        return Ret(Error.OK, o)

    def set_default(self, o_user):
        """
        设为默认银行卡
        """
        if self.owner != o_user:
            return Ret(Error.NOT_YOUR_CARD)
        self.owner.default_card = self
        self.owner.save()
        return Ret()

    def safe_delete(self, o_user):
        """
        安全删除银行卡
        """
        if self.owner != o_user:
            return Ret(Error.NOT_YOUR_CARD)
        if self.owner.default_card == self:
            self.owner.default_card = None
            self.owner.save()
        self.delete()
        return Ret()
