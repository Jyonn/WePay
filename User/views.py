import re

from User.models import User
from base.captcha import SendMobile
from base.common import login_to_session, logout_user_from_session, get_user_from_session
from base.decorator import require_json, require_params, require_buyer, require_login
from base.error import Error
from base.response import error_response, response
from base.session import save_captcha, save_session, check_captcha


@require_json
@require_params(['phone'])
def send_captcha(request):
    """
    发送验证码
    """
    phone = request.POST['phone']
    phone_regex = '^1[34578]\d{9}$'
    if re.search(phone_regex, phone) is None:
        return error_response(Error.PHONE_FORMAT)  # 手机格式错误
    ret_code, phone_captcha = SendMobile.send_captcha(phone)
    if ret_code != 0:
        return error_response(Error.ERROR_SEND_PHONE_CAPTCHA)  # 发送错误
    save_captcha(request, 'phone', phone_captcha)
    save_session(request, 'phone', phone)
    return response()


@require_json
@require_params(['password', 'is_seller', 'brand', 'username', 'captcha'])
def register(request):
    """
    注册
    """
    password = request.POST['password']
    is_seller = request.POST['is_seller'] == '1'
    if is_seller:  # 商家
        brand = request.POST['brand']
        username = request.POST['username']
        ret = User.create(username, password, User.TYPE_SELLER, brand)
    else:  # 买家
        captcha = request.POST['captcha']
        phone = request.POST['phone']
        if not check_captcha(request, 'phone', captcha):
            return error_response(Error.ERROR_PHONE_CAPTCHA)  # 验证码错误
        ret = User.create(phone, password, User.TYPE_BUYER)
    return response(body=ret.body.pk) if ret.error == Error.OK else error_response(ret.error)


@require_json
@require_params(['username', 'password'])
def login(request):
    """
    登录
    """
    username = request.POST['username']
    password = request.path['password']
    ret = User.check_password(username, password)
    if ret.error == Error.OK:
        login_to_session(request, ret.body)
    return response(body=ret.body.pk) if ret.error == Error.OK else error_response(ret.error)


@require_login
def logout(request):
    """
    登出
    """
    logout_user_from_session(request)
    return response()


@require_json
@require_params(['real_name', 'address'])
@require_buyer
def edit_address(request):
    """
    买家编辑收货信息
    """
    real_name = request.POST['real_name']
    address = request.POST['address']
    o_user = get_user_from_session(request)
    ret = o_user.edit_info(address, real_name)
    return response() if ret.error == Error.OK else error_response(ret.error)


@require_buyer
def get_address(request):
    """
    买家获取收获信息
    """
    o_user = get_user_from_session(request)
    ret = o_user.get_info()
    return response(body=ret.body) if ret.error == Error.OK else error_response(ret.error)
