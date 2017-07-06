import re

from User.models import User
from base.captcha import SendMobile
from base.common import login_to_session, logout_user_from_session, get_user_from_session
from base.decorator import require_json, require_params, require_buyer
from base.error import Error
from base.response import error_response, response
from base.session import save_captcha, save_session, check_captcha


@require_json
@require_params(['phone'])
def send_captcha(request):
    phone = request.POST['phone']
    phone_regex = '^1[3458]\d{9}$'
    if re.search(phone_regex, phone) is None:
        return error_response(Error.PHONE_FORMAT)
    ret_code, phone_captcha = SendMobile.send_captcha(phone)
    if ret_code != 0:
        return error_response(Error.ERROR_SEND_PHONE_CAPTCHA)
    save_captcha(request, 'phone', phone_captcha)
    save_session(request, 'phone', phone)
    return response()


@require_json
@require_params(['password', 'is_seller', 'brand', 'username', 'captcha'])
def register(request):
    password = request.POST['password']
    is_seller = request.POST['is_seller'] == '1'
    if is_seller:
        brand = request.POST['brand']
        username = request.POST['username']
        ret = User.create(username, password, User.TYPE_SELLER, brand)
    else:
        captcha = request.POST['captcha']
        phone = request.POST['phone']
        if not check_captcha(request, 'phone', captcha):
            return error_response(Error.ERROR_PHONE_CAPTCHA)
        ret = User.create(phone, password, User.TYPE_BUYER)
    return response(body=ret.body.pk) if ret.error == Error.OK else error_response(ret.error)


@require_json
@require_params(['username', 'password'])
def login(request):
    username = request.POST['username']
    password = request.path['password']
    ret = User.check_password(username, password)
    if ret.error == Error.OK:
        login_to_session(request, ret.body)
    return response(body=ret.body.pk) if ret.error == Error.OK else error_response(ret.error)


def logout(request):
    logout_user_from_session(request)


@require_json
@require_params(['real_name', 'address'])
@require_buyer
def edit_address(request):
    real_name = request.POST['real_name']
    address = request.POST['address']
    o_user = get_user_from_session(request)
    ret = o_user.edit_info(address, real_name)
    return response() if ret.error == Error.OK else error_response(ret.error)


@require_buyer
def get_address(request):
    o_user = get_user_from_session(request)
    ret = o_user.get_info()
    return response(body=ret.body) if ret.error == Error.OK else error_response(ret.error)
