# -*-Coding:UTF-8 -*-
"""
程序：七牛云
版本：1.0
作者：鬼义虎神
日期：2019年8月21日
功能：
    1. 上传图片到七牛云
"""
from flask_restful import current_app
from qiniu import Auth, put_file, etag, put_data, put_stream
import qiniu.config


def upload_image(image_stream):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = current_app.config.get('QINIU_ACCESS_KEY')
    secret_key = current_app.config.get('QINIU_SECRET_KEY')
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = current_app.config.get('QINIU_BUCKET_NAME')
    # 上传后保存的文件名
    key = None
    # 生成上传 Token，可以指定过期时间等，设置5天的过期时间，因为Linux的时间比真实时间慢
    token = q.upload_token(bucket_name, key, 432000)
    # 要上传文件的本地路径
    # localfile = './sync/bbb.jpg'
    # ret, info = put_file(token, key, localfile)
    # 我们不是用文件上传，使用二进制流上传
    result, info = put_data(up_token=token, key=key, data=image_stream)
    print('ret：', result)
    print("info：", info)

    # 返回图片的文件名
    return result['key']

"""在Python Console中测试"""
# from utils.qiniu import upload_image
# from toutiao.main import  app
# # with open('/home/python/lyj.jpg', 'rb') as f:
# #     image_stream = f.read()
# # with app.app_context():
# #     image_name = upload_image(image_stream)
