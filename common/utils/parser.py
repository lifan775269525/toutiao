# -*-Coding:UTF-8 -*-
"""
程序：自定应类型验证的类
版本：1.0
作者：鬼义虎神
日期：2019年8月20日
功能：
    1. 结合flask_restful的reqparser中的type使用
"""
import re


def moblie(mobile):
    """
    验证手机号格式
    :return: mobile
    """
    if re.match(r'^1[3-9]\d{9}$', mobile):
        return mobile
    else:
        return ValueError(f'{mobile} is not valid moblie')
