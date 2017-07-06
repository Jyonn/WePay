def save_session(request, key, value):
    """
    保存数据到session
    :param key: 键
    :param value: 值
    """
    request.session["saved_" + key] = value


def load_session(request, key, once_delete=True):
    """
    加载session中的键值
    :param key: 键
    :param once_delete: 加载后删除
    :return: 值
    """
    value = request.session.get("saved_" + key)
    if value is None:
        return None
    if once_delete:
        del request.session["saved_" + key]
    return value


def login_to_session(request, admin):
    """
    登录
    :param admin: Admin类
    """
    try:
        request.session.cycle_key()
    except:
        pass
    save_session(request, 'admin', admin.pk)
    return None
