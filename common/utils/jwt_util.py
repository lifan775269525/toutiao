# -*-Coding:UTF-8 -*-
"""
程序：JWT的加密与解密工具类
版本：1.0
作者：鬼义虎神
日期：2019年8月20日
功能：
    1. 加密JWT--生成JWT
    2. 解密JWT--校验JWT
"""
import jwt
from flask import current_app


# 生成JWT
def generate_jwt(payload, expiry, secret=None):
    """
    生成jwt
    :param payload: dict 载荷
    :param expiry: datetime 有效期
    :param secret: 密钥
    :return: jwt
    """
    # 过期时间exp是jwt标准版注册声明过期事件的
    _payload = {'exp': expiry}
    # 更新_payload，注意update没有返回值，直接更改原字典
    _payload.update(payload)

    # 如果没有指定加密密钥，我们获取默认配置的密钥
    if secret is None:
        secret = current_app.config.get("JWT_SECRET")

    # 返回的是字节流
    encode_jwt_b = jwt.encode(_payload, secret, algorithm='HS256')

    return encode_jwt_b.decode()


def verify_jwt(token, secret=None):
    """
    检验jwt
    :param token: jwt
    :param secret: 密钥
    :return: dict: payload
    """
    # 如果没有指定加密密钥，我们获取默认配置的密钥
    if secret is None:
        secret = current_app.config.get("JWT_SECRET")
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
    except jwt.PyJWTError as err:
        current_app.logger.error('JWT解密失败，返回为None的Payload。')
        payload = None

    return payload
