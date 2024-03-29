# -*-Coding:UTF-8 -*-
"""
程序：用户蓝图的初始化文件
版本：1.0
作者：鬼义虎神
日期：2019年8月20日
功能：
    1. 设置路由规则
"""
from flask import Blueprint
from flask_restful import Api

from toutiao.resources.user import passport, profle
from toutiao.resources.user.output import output_json

user_bp = Blueprint('user', __name__)
user_api = Api(user_bp, catch_all_404s=True)

# 装饰器的灵魂代码，代替装饰器
user_api.representation('application/json')(output_json)

"""注册路由"""
# 用户登录
user_api.add_resource(passport.AuthorizationResource, '/v1_0/authorizations', endpoint='Authorization')
# 上传头像
user_api.add_resource(profle.PhotoResource, '/v1_0/user/photo', endpoint='Photo')
# 获取用户信息
user_api.add_resource(profle.UserResource, '/v1_0/users/<int(min=1):user_id>', endpoint='User')
