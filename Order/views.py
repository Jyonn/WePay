from Good.models import Category
from Order.models import Order
from User.models import User
from base.common import get_user_from_session
from base.decorator import require_json, require_params, require_login, require_seller, require_buyer
from base.error import Error
from base.response import error_response, response


@require_json
@require_params(['user_id', 'category_id'])
def add_order(request):
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


@require_login
def get_order_list(request, status, page):
    if status not in ['unsent', 'unreceived']:
        return error_response(Error.ERROR_STATUS)
    status = Order.STATUS_CONFIRM_ORDER_BY_SELLER if status == 'unsent' else Order.STATUS_CONFIRM_DELIVER

    o_user = get_user_from_session(request)
    ret = o_user.get_order_list(status, page)
    return response(body=ret.body) if ret.error == Error.OK else error_response(ret.error)


@require_seller
def confirm_send(request, order_id):
    ret = Order.get(order_id)
    if ret.error != Error.OK:
        return error_response(ret.error)
    o_order = ret.body

    o_user = get_user_from_session(request)
    ret = o_order.confirm_send(o_user)
    return response() if ret.error else error_response(ret.error)


@require_buyer
def confirm_receive(request, order_id):
    ret = Order.get(order_id)
    if ret.error != Error.OK:
        return error_response(ret.error)
    o_order = ret.body

    o_user = get_user_from_session(request)
    ret = o_order.confirm_receive(o_user)
    return response() if ret.error else error_response(ret.error)
