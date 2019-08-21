# -*-Coding:UTF-8 -*-
"""
程序：请求钩子/中间件
版本：1.0
作者：鬼义虎神
日期：2019年8月21日
功能：
    1. 对每次请求都进行加工
    before_first_request
    before_request
    after_request
    teardown_request
"""
from flask import g, request

from utils.jwt_util import verify_jwt


def jwt_authentication():
    """根据jwt验证用户身份"""
    g.user_id = None
    g.is_refresh_token = False
    # 从请求头中获取参数
    authorization = request.headers.get('Authorization')
    if authorization and authorization.startswith('Bearer '):
        token = authorization.split(" ")[-1]
        payload = verify_jwt(token)
        if payload:
            g.user_id = payload.get('user_id')
            g.is_refresh_token = payload.get('is_refresh')

    pass
