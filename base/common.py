from User.models import User
from base.session import load_session


def get_user_from_session(request):
    """
    获取session中的Admin
    :param request:
    :return:
    """
    user_id = load_session(request, 'user', once_delete=False)
    if user_id is None:
        return None
    try:
        return User.objects.get(pk=user_id)
    except:
        return None


def logout_user_from_session(request):
    """
    登出
    """
    load_session(request, 'admin')
