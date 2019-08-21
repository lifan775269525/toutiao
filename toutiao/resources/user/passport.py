# -*-Coding:UTF-8 -*-
"""
程序：
版本：1.0
作者：鬼义虎神
日期：
功能：
    1. 
"""
from flask_restful import Resource, current_app, reqparse, inputs

from utils import parser


# 用户视图类
class AuthorizationResource(Resource):

    def get(self):
        print('进入用户认证模块')
        return '进入用户认证模块'

    def post(self):
        """登录、注册创建token（JWT）"""
        # 接收参数、校验参数
        rep = reqparse.RequestParser()
        # 验证手机号
        rep.add_argument('mobile', required=True, type=parser.moblie, location='json')
        # 验证验证码
        rep.add_argument('code', required=True, type=inputs.regex(r'^\d{6}$'), location='json')
        # 启用验证
        args = rep.parse_args()
        # 获取校验后的参数
        mobile = args.mobile
        code = args.code
        print()

        # 数据处理
        # 根据mobile组合成key，去redis中取code


        # 返回响应
        pass
