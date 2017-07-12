import base64
from functools import wraps

from django.views.decorators import http

from User.models import User
from base.common import get_user_from_session
from base.response import *

require_post = http.require_POST
require_get = http.require_GET


def require_params(r_params):
    """
    需要获取的参数是否在request.POST中存在
    """
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            for require_param in r_params:
                if require_param not in request.POST:
                    return error_response(Error.REQUIRE_PARAM, append_msg=require_param)
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_get_params(r_params):
    """
    需要获取的参数是否在request.GET中存在
    """
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            for require_param in r_params:
                if require_param not in request.GET:
                    return error_response(Error.REQUIRE_PARAM, append_msg=require_param)
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def require_json(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if request.body:
            try:
                request.POST = json.loads(request.body.decode())
            except:
                pass
            return func(request, *args, **kwargs)
        else:
            return error_response(Error.REQUIRE_JSON)

    return wrapper


def decorator_generator(verify_func, error_id):
    """
    装饰器生成器
    """
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            print("verify")
            if verify_func(request):
                return func(request, *args, **kwargs)
            print(error_id)
            return error_response(error_id)
        return wrapper
    return decorator


def require_login_func(request):
    """
    需要登录装饰器
    """
    o_user = get_user_from_session(request)
    return o_user is not None


def require_buyer_func(request):
    """
    需要买家登录装饰器
    """
    print("require")
    o_user = get_user_from_session(request)
    print(o_user.pk)
    return o_user is not None and o_user.user_type == User.TYPE_BUYER


def require_seller_func(request):
    """
    需要商家登录装饰器
    """
    o_user = get_user_from_session(request)
    return o_user is not None and o_user.user_type == User.TYPE_SELLER

require_login = decorator_generator(require_login_func, Error.REQUIRE_LOGIN)
require_buyer = decorator_generator(require_buyer_func, Error.REQUIRE_BUYER)
require_seller = decorator_generator(require_seller_func, Error.REQUIRE_SELLER)
