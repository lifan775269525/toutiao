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
import imghdr
from flask import current_app


# 验证是否是图片格式
def image_file(file_path):
    """
    验证是否是图片
    :param file_path: 文件路径
    :return:
    """
    try:
        image_type = imghdr.what(file_path)
    except Exception as err:
        current_app.logger.warn('上传的图片类型无效')
        return {"message": '不是图片'}
    else:
        if image_type:
            return file_path
        else:
            current_app.logger.warn('上传的图片类型无效')
            return {"message": '不是图片'}


# 验证是否是手机
def moblie(mobile):
    """
    验证手机号格式
    :return: mobile
    """
    if re.match(r'^1[3-9]\d{9}$', mobile):
        return mobile
    else:
        return ValueError(f'{mobile} is not valid moblie')
