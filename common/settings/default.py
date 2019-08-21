# -*-Coding:UTF-8 -*-
"""
程序：Flask默认的配置文件
版本：1.0
作者：鬼义虎神
日期：2019年8月20日
功能：
    1. Flask项目基础的配置类
"""


class DefaultConfig(object):
    # 日志配置信息
    LOGGING_LEVEL = 'DEBUG'
    LOGGING_FILE_DIR = '/home/python/logs'
    LOGGING_FILE_MAX_BYTES = 300 * 1024 * 1024
    LOGGING_FILE_BACKUP = 10

    # JWT配置信息
    JWT_SECRET = 'TPmi4aLWRbyVq8zu9v82dWYW17/z+UvRnYTt4P6fAXA'  # 密钥
    # 业务token过期时间
    # 刷新token过期时间
