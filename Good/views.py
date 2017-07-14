from Good.models import Category, Good, Button
from base.c_qiniu import QiNiu
from base.common import get_user_from_session, get_pic_url_from_request
from base.decorator import require_json, require_params, require_seller, require_buyer, require_get_params
from base.error import Error
from base.response import response, error_response


def init_category(request):
    """
    商品类别初始化
    """
    ret = Category.init()
    return response() if ret.error == Error.OK else error_response(ret.error)


@require_get_params(['type'])
def get_category_list(request):
    """
    获取商品类别列表
    """
    _type = request.GET['type']
    if _type not in ['all', 'unset']:
        return error_response(Error.ERROR_TYPE)
    if _type == 'all':
        ret = Category.get_list()
    else:
        o_user = get_user_from_session(request)
        if o_user is None:
            return error_response(Error.REQUIRE_LOGIN)
        ret = Category.get_unset_list(o_user)
    return response(body=ret.body) if ret.error == Error.OK else error_response(ret.error)


def get_good_of_category(request, category_id):
    """
    获取一个类别的所有商品
    """
    ret = Category.get(category_id)
    if ret.error != Error.OK:
        return error_response(ret.error)

    o_category = ret.body
    ret = o_category.get_good_list()
    return response(body=ret.body) if ret.error == Error.OK else error_response(ret.error)


@require_json
@require_params(['category_id', 'good_name', 'price', 'store', 'description', 'pic', 'gzipped'])
@require_seller
def add_good(request):
    """
    商家添加商品
    """
    category_id = request.POST['category_id']
    name = request.POST['good_name']
    price = request.POST['price']
    store = request.POST['store']
    description = request.POST['description']
    pic = request.POST['pic']
    gzipped = request.POST['gzipped'] == '1'

    ret = Category.get(category_id)
    if ret.error != Error.OK:
        return error_response(ret.error)
    o_category = ret.body

    if pic == '':
        pic_key = ''
    else:
        ret = get_pic_url_from_request(pic, gzipped)
        if ret.error != Error.OK:
            return error_response(ret.error)
        pic_key = ret.body

    o_user = get_user_from_session(request)
    ret = Good.create(o_user, o_category, name, price, store, pic_key, description)
    if ret.error != Error.OK:
        QiNiu.delete(pic_key)
        return error_response(ret.error)
    return response(body=ret.body.pk)


@require_json
@require_params(['name', 'price', 'store', 'description', 'pic', 'gzipped'])
@require_seller
def edit_good(request, good_id):
    """
    商家编辑商品
    """
    ret = Good.get(good_id)
    if ret.error != Error.OK:
        return error_response(ret.error)
    o_good = ret.body

    name = request.POST['name']
    price = request.POST['price']
    store = request.POST['store']
    description = request.POST['description']
    pic = request.POST['pic']
    gzipped = request.POST['gzipped'] == '1'

    if pic == "":
        pic_key = o_good.pic
    else:
        ret = get_pic_url_from_request(pic, gzipped)
        if ret.error != Error.OK:
            return error_response(ret.error)
        pic_key = ret.body

    o_user = get_user_from_session(request)
    ret = o_good.edit_info(o_user, name, price, store, description, pic_key)
    return response() if ret.error == Error.OK else error_response(ret.error)


@require_seller
def delete_good(request, good_id):
    """
    商家删除商品
    """
    ret = Good.get(good_id)
    if ret.error != Error.OK:
        return error_response(ret.error)
    o_good = ret.body

    o_user = get_user_from_session(request)
    ret = o_good.lazy_remove(o_user)
    return response() if ret.error == Error.OK else error_response(ret.error)


@require_seller
def get_good_list(request):
    """
    商家获取商品列表
    """
    o_user = get_user_from_session(request)
    ret = o_user.get_good_list()
    return response(body=ret.body) if ret.error == Error.OK else error_response(ret.error)


def get_single_good(request, good_id):
    """
    获取单一商品信息
    """
    ret = Good.get(good_id)
    if ret.error != Error.OK:
        return error_response(ret.error)
    o_good = ret.body
    ret = o_good.get_info()
    return response(body=ret.body) if ret.error == Error.OK else error_response(ret.error)


@require_json
@require_params(['good_id', 'number'])
@require_buyer
def add_button(request):
    """
    买家添加设置按钮
    """
    good_id = request.POST['good_id']
    number = request.POST['number']

    ret = Good.get(good_id)
    if ret.error != Error.OK:
        return error_response(ret.error)
    o_good = ret.body

    o_user = get_user_from_session(request)
    ret = Button.create(o_user, o_good, number)

    return response(body=ret.body.pk) if ret.error == Error.OK else error_response(ret.error)


@require_json
@require_params(['good_id', 'number'])
@require_buyer
def edit_button(request, button_id):
    """
    买家编辑设置按钮
    """
    good_id = request.POST['good_id']
    number = request.POST['number']

    ret = Good.get(good_id)
    if ret.error != Error.OK:
        return error_response(ret.error)
    o_good = ret.body

    ret = Button.get(button_id)
    if ret.error != Error.OK:
        return error_response(ret.error)
    o_button = ret.body

    o_user = get_user_from_session(request)
    ret = o_button.edit_info(o_user, o_good, number)

    return response() if ret.error == Error.OK else error_response(ret.error)


@require_buyer
def delete_button(request, button_id):
    """
    买家删除设置按钮
    """
    ret = Button.get(button_id)
    if ret.error != Error.OK:
        return error_response(ret.error)
    o_button = ret.body

    o_user = get_user_from_session(request)
    ret = o_button.remove(o_user)

    return response() if ret.error == Error.OK else error_response(ret.error)


@require_buyer
def get_button_list(request):
    """
    买家获取设置按钮列表
    """
    o_user = get_user_from_session(request)
    ret = o_user.get_button_list()
    return response(body=ret.body) if ret.error == Error.OK else error_response(ret.error)
