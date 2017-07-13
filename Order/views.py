from Good.models import Category
from Order.models import Order
from User.models import User
from base.common import get_user_from_session
from base.decorator import require_json, require_params, require_login, require_seller, require_buyer, \
    require_get_params
from base.error import Error
from base.response import error_response, response


@require_json
@require_params(['user_id', 'category_id'])
def add_order(request):
    """
    按钮新增订单
    """
    user_id = request.POST['user_id']
    category_id = request.POST['category_id']

    ret = User.get(user_id)
    if ret.error != Error.OK:
        return error_response(ret.error)
    o_user = ret.body

    ret = Category.get(category_id)
    if ret.error != Error.OK:
        return error_response(ret.error)
    o_category = ret.body

    ret = Order.create(o_user, o_category)
    return response(body=ret.body.pk) if ret.error == Error.OK else error_response(ret.error)


@require_get_params(['status', 'exist', 'count'])
@require_seller
def get_seller_order_list(request):
    """
    商家获取订单列表
    """
    status = request.GET['status']
    exist = request.GET['exist']
    count = request.GET['count']
    if status not in ['unsent', 'unreceived']:
        return error_response(Error.ERROR_STATUS)
    status = Order.STATUS_CONFIRM_ORDER_BY_SELLER if status == 'unsent' else Order.STATUS_CONFIRM_DELIVER

    o_user = get_user_from_session(request)
    ret = o_user.get_order_list(status, exist, count)
    return response(body=ret.body) if ret.error == Error.OK else error_response(ret.error)


@require_get_params(['status'])
@require_buyer
def get_buyer_order_list(request):
    """
    买家获取订单列表
    """
    status = request.GET['status']
    if status not in ['unsent', 'unreceived']:
        return error_response(Error.ERROR_STATUS)
    status = Order.STATUS_CONFIRM_ORDER_BY_SELLER if status == 'unsent' else Order.STATUS_CONFIRM_DELIVER

    o_user = get_user_from_session(request)
    ret = o_user.get_order_list(status)
    return response(body=ret.body) if ret.error == Error.OK else error_response(ret.error)


@require_seller
def confirm_send(request, order_id):
    """
    商家确认发货
    """
    ret = Order.get(order_id)
    if ret.error != Error.OK:
        return error_response(ret.error)
    o_order = ret.body

    o_user = get_user_from_session(request)
    ret = o_order.confirm_send(o_user)
    return response() if ret.error else error_response(ret.error)


@require_buyer
def confirm_receive(request, order_id):
    """
    买家确认收获
    """
    ret = Order.get(order_id)
    if ret.error != Error.OK:
        return error_response(ret.error)
    o_order = ret.body

    o_user = get_user_from_session(request)
    ret = o_order.confirm_receive(o_user)
    return response() if ret.error else error_response(ret.error)
