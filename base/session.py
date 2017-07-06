import datetime


def save_session(request, key, value):
    """
    保存数据到session
    """
    request.session["saved_" + key] = value


def load_session(request, key, once_delete=True):
    """
    加载session中的键值
    """
    value = request.session.get("saved_" + key)
    if value is None:
        return None
    if once_delete:
        del request.session["saved_" + key]
    return value


def save_captcha(request, captcha_type, code, last=300):
    """
    保存验证码
    :param request:
    :param last: 有效期限
    :param captcha_type: 验证码类型，分为 image_register, image_forget 和 phone_register, phone_forget
    :param code: 验证码值
    :return: None
    """
    request.session["saved_" + captcha_type + "_code"] = str(code)
    request.session["saved_" + captcha_type + "_time"] = int(datetime.datetime.now().timestamp())
    request.session["saved_" + captcha_type + "_last"] = last
    return None


def check_captcha(request, captcha_type, code):
    """
    检验验证码
    :param request:
    :param captcha_type: 验证码类型，分为 image_register, image_forget 和 phone
    :param code: 验证码值
    :return: 相同返回True, 不同返回False
    """
    correct_code = request.session.get("saved_" + captcha_type + "_code")
    correct_time = request.session.get("saved_" + captcha_type + "_time")
    correct_last = request.session.get("saved_" + captcha_type + "_last")
    current_time = int(datetime.datetime.now().timestamp())
    # print(correct_time, correct_last, correct_code, current_time)
    try:
        del request.session["saved_" + captcha_type + "_code"]
        del request.session["saved_" + captcha_type + "_time"]
        del request.session["saved_" + captcha_type + "_last"]
    except:
        pass
    if None in [correct_code, correct_time, correct_last]:
        return False
    if current_time - correct_time > correct_last:
        return False
    return correct_code.upper() == str(code).upper()
