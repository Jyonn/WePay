import base64
import os

from django.utils.crypto import get_random_string

from User.models import User
from WePay.settings import PIC_PATH, PIC_MAX_SIZE
from base.c_qiniu import QiNiu
from base.error import Error
from base.response import Ret
from base.session import load_session, save_session


def save_file_to_local(save_file, file_path):
    with open(file_path, "wb+") as f:
        for chunk in save_file.chunks():
            f.write(chunk)
        f.close()
    return


def upload_good_pic(raw_pic):
    random_string = get_random_string(length=16)
    file_path = os.path.join(PIC_PATH, random_string)
    save_file_to_local(raw_pic, file_path)

    import imghdr
    img_type = imghdr.what(file_path)
    if img_type not in ["jpeg", "png", "bmp"]:
        os.remove(file_path)
        return Ret(Error.ILLEGAL_PIC)
    key = 'aks/good/image/' + random_string
    ret = QiNiu.upload(key, file_path)
    os.remove(file_path)
    return Ret(Error.OK, key) if ret else Ret(Error.FAILED_UPLOAD)


def get_pic_url_from_request(pic, gzipped):
    try:
        pic = base64.decodebytes(bytes(pic, encoding='utf8'))
        if gzipped:
            import gzip
            pic = gzip.decompress(pic)
        if len(pic) > PIC_MAX_SIZE:
            return Ret(Error.PIC_SIZE)

        ret = upload_good_pic(pic)
        if ret.error != Error.OK:
            return Ret(ret.error)
        pic_key = ret.body
    except:
        return Ret(Error.ILLEGAL_PIC)
    return Ret(Error.OK, pic_key)


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


def login_to_session(request, user):
    """
    登录到session
    """
    try:
        request.session.cycle_key()
    except:
        pass
    save_session(request, 'user', user.pk)
    return None


def logout_user_from_session(request):
    """
    登出
    """
    load_session(request, 'user')
