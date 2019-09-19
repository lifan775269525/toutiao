# -*-Coding:UTF-8 -*-
"""
程序：
版本：1.0
作者：鬼义虎神
日期：
功能：
    1. 
"""
from flask import g
from flask_restful import Resource, reqparse, current_app

# ORM映射SQLAlchemy对象
from models import db
# 类型验证
from utils import parser
# 用户模型类
from models.user import User
# 缓存工具类
from cache.user import UserCache
# 上传图片到七牛云
from utils.qiniu import upload_image
# 验证登录装饰器
from utils.decorators import login_required


# 上传图片
class PhotoResource(Resource):
    """
    用户图像 （头像，身份证）
    """
    # 登录验证
    method_decorators = [login_required]

    def patch(self):
        """

        :return:
        """
        """接收参数、验证参数"""
        rep = reqparse.RequestParser()
        rep.add_argument('image', required=True, action='store', type=parser.image_file, help='图片必传', location='files')
        args = rep.parse_args()
        image = args.get('image')

        """数据处理"""
        # 上传到七牛云
        image_stream = image.read()
        try:
            image_name = upload_image(image_stream)
        except Exception as err:
            current_app.logger.error('上传图片失败！')
            print('上传图片失败！')
            return {"message": '上传图片失败'}

        # 保存到数据库
        try:
            user = User.query.get(g.user_id)
            user.profile_photo = image_name
            db.session.add(user)
            db.session.commit()
        except Exception as err:
            current_app.logger.error('保存图片名字到数据库失败，开始回滚')
            print('保存图片名字到数据库失败，开始回滚')
            db.session.rollback()
            return {"message": '保存图片名称到数据库失败'}

        """返回响应"""
        photo_url = current_app.config.get('QINIU_DOMAIN') + image_name
        print('图片最终的地址：', photo_url)
        return {'photo_url': photo_url}


# 获取用户信息
class UserResource(Resource):
    """
    获取用户信息
    """
    # 登录验证
    method_decorators = [login_required]

    def get(self, user_id):
        user_cache = UserCache(user_id)
        if user_cache.is_exist():
            return user_cache.get()
        else:
            return {'message': "用户不存在"}
