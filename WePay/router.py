from Card.views import add_card, get_card_list, set_default_card, delete_card
from Good.views import get_category_list, get_good_of_category, add_good, edit_good, delete_good, get_good_list, \
    add_button, edit_button, delete_button, get_button_list
from Order.views import add_order, get_order_list, confirm_send, confirm_receive
from User.models import User
from User.views import send_captcha, register, login, logout, edit_address, get_address
from base.common import get_user_from_session
from base.decorator import require_login
from base.error import Error
from base.response import error_response


def session(request):
    if request.method == 'PUT':  # 发送验证码
        return send_captcha(request)
    elif request.method == 'POST':  # 用户登录
        return login(request)
    elif request.method == 'DELETE':  # 用户退出
        return logout(request)
    else:
        return error_response(Error.ERROR_METHOD)


def user(request):
    if request.method == 'POST':  # 用户注册
        return register(request)
    else:
        return error_response(Error.ERROR_METHOD)


def user_address(request):
    if request.method == 'PUT':  # 编辑收货信息
        return edit_address(request)
    elif request.method == 'GET':  # 获取收货信息
        return get_address(request)
    else:
        return error_response(Error.ERROR_METHOD)


def card(request):
    if request.method == 'POST':  # 新增银行卡
        return add_card(request)
    elif request.method == 'GET':  # 获取银行卡列表
        return get_card_list(request)
    else:
        return error_response(Error.ERROR_METHOD)


def user_default_card(request):
    if request.method == 'PUT':  # 设置默认银行卡
        return set_default_card(request)
    else:
        return error_response(Error.ERROR_METHOD)


def card_card_id(request, card_id):
    if request.method == 'DELETE':  # 删除银行卡
        return delete_card(request, card_id)
    else:
        return error_response(Error.ERROR_METHOD)


def category(request):
    if request.method == 'GET':  # 获取商品类别列表
        return get_category_list(request)
    else:
        return error_response(Error.ERROR_METHOD)


def category_category_id_good(request, category_id):
    if request.method == 'GET':  # 获取一个类别的所有商品
        return get_good_of_category(request, category_id)
    else:
        return error_response(Error.ERROR_METHOD)


def good(request):
    if request.method == 'POST':  # 新增商品
        return add_good(request)
    elif request.method == 'GET':  # 商家获取商品列表
        return get_good_list(request)
    else:
        return error_response(Error.ERROR_METHOD)


def good_good_id(request, good_id):
    if request.method == 'PUT':  # 编辑商品
        return edit_good(request, good_id)
    elif request.method == 'DELETE':
        return delete_good(request, good_id)
    else:
        return error_response(Error.ERROR_METHOD)


def button(request):
    if request.method == 'POST':  # 新增按钮
        return add_button(request)
    elif request.method == 'GET':  # 获取按钮列表
        return get_button_list(request)
    else:
        return error_response(Error.ERROR_METHOD)


def button_button_id(request, button_id):
    if request.method == 'PUT':  # 编辑按钮
        return edit_button(request, button_id)
    elif request.method == 'DELETE':
        return delete_button(request, button_id)
    else:
        return error_response(Error.ERROR_METHOD)


def order(request):
    if request.method == 'POST':  # 新增订单
        return add_order(request)
    else:
        return error_response(Error.ERROR_METHOD)


def order_status_page(request, status, page):
    if request.method == 'GET':  # 查看订单列表
        return get_order_list(request, status, page)
    else:
        return error_response(Error.ERROR_METHOD)


@require_login
def order_order_id_status(request, order_id):
    o_user = get_user_from_session(request)
    if request.method == 'PATCH':  # 确认收发商品
        if o_user.user_type == User.TYPE_SELLER:
            return confirm_send(request, order_id)
        else:
            return confirm_receive(request, order_id)
    else:
        return error_response(Error.ERROR_METHOD)

