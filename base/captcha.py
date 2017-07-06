import json
from urllib.parse import urlencode

import requests
from django.utils.crypto import get_random_string

from base.base_settings import yunpian_appkey


class SendMobile:
    """
    手机验证码发送类
    """
    @staticmethod
    def send_captcha(mobile):
        """
        发送验证码
        :param mobile: 手机号
        :return: 发送是否成功
        """
        text = "【浙江大学智能按钮】您的验证码是#code#。有效时间为5分钟"
        phone_code = get_random_string(length=6, allowed_chars="1234567890")
        text = text.replace("#code#", phone_code)
        ret_code = SendMobile.send_sms(yunpian_appkey, text, mobile)
        return ret_code, phone_code

    @staticmethod
    def send_sms(apikey, text, mobile):
        """
        云片短信发送API
        :param apikey: 云片应用密钥
        :param text: 发送明文
        :param mobile: 11位手机号
        :return: 发送是否成功
        """
        # 服务地址
        url = "https://sms.yunpian.com/v2/sms/single_send.json"
        params = urlencode({'apikey': apikey, 'text': text, 'mobile': mobile})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "application/json"}
        response = requests.post(url, params, headers=headers)
        response_str = response.text
        response.close()
        try:
            ret_code = json.loads(response_str)['code']
        except:
            return -1
        return ret_code
