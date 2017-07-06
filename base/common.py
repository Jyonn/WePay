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
    """
    保存文件到本地
    :param save_file: 文件二进制流
    :param file_path: 文件保存地址
    """
    with open(file_path, "wb+") as f:
        for chunk in save_file.chunks():
            f.write(chunk)
        f.close()


def upload_good_pic(raw_pic):
    """
    上传文件流到七牛
    :param raw_pic: 图片二进制流
    :return: 上传成功返回键值，失败返回错误参数
    """
    random_string = get_random_string(length=16)  # 随机键值
    file_path = os.path.join(PIC_PATH, random_string)
    save_file_to_local(raw_pic, file_path)  # 保存到本地

    import imghdr
    img_type = imghdr.what(file_path)  # 判断图片类型
    if img_type not in ["jpeg", "png", "bmp"]:
        os.remove(file_path)
        return Ret(Error.ILLEGAL_PIC)  # 不是正确的图片
    key = 'aks/good/image/' + random_string
    ret = QiNiu.upload(key, file_path)
    os.remove(file_path)  # 删除本地文件
    return Ret(Error.OK, key) if ret else Ret(Error.FAILED_UPLOAD)


def get_pic_url_from_request(pic, gzipped):
    """
    解封图片流并保存到七牛
    :param pic: Base64编码过的图片字符串
    :param gzipped: 是否经过gZip压缩
    :return: 成功则返回键值，失败返回错误参数
    """
    try:
        pic = base64.decodebytes(bytes(pic, encoding='utf8'))  # base64解码
        if gzipped:  # 如果经过gZip压缩，解压缩
            import gzip
            pic = gzip.decompress(pic)
        if len(pic) > PIC_MAX_SIZE:
            return Ret(Error.PIC_SIZE)  # 图片过大

        ret = upload_good_pic(pic)  # 上传图片
        if ret.error != Error.OK:
            return Ret(ret.error)
        pic_key = ret.body
    except:
        return Ret(Error.ILLEGAL_PIC)
    return Ret(Error.OK, pic_key)


def get_user_from_session(request):
    """
    获取session中的Admin
    :return: 用户类
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
