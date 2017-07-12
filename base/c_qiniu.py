from qiniu import Auth, put_file, etag
from qiniu import BucketManager

from base.base_settings import qiniu_access_key, qiniu_secret_key


class QiNiu:
    """
    七牛类
    """
    bucket_name = 'image'  # 七牛仓库名
    host = 'https://image.6-79.cn/'  # 七牛HOST
    q = Auth(qiniu_access_key, qiniu_secret_key)

    @staticmethod
    def upload(key, local_file):
        """
        上传文件
        :param key: 键值
        :param local_file: 文件
        0.
        :return: 上传是否成功
        """
        print('--upload--')
        token = QiNiu.q.upload_token(QiNiu.bucket_name, key, 3600)
        ret, info = put_file(token, key, local_file)
        print(ret, info)
        return ret['key'] == key and ret['hash'] == etag(local_file)

    @staticmethod
    def delete(key):
        """
        删除文件
        :param key: 键值
        :return: 删除是否成功
        """
        bucket = BucketManager(QiNiu.q)
        ret, info = bucket.delete(QiNiu.bucket_name, key)
        return ret == {}
