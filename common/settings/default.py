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
    JWT_EXPIRY_HOURS = 2
    # 刷新token过期时间
    JWT_REFRESH_DAYS = 14

    # Redis哨兵配置信息
    REDIS_SENTINELS = [
        ('127.0.0.1', '26380'),
        ('127.0.0.1', '26381'),
        ('127.0.0.1', '26382'),
    ]
    REDIS_SENTINEL_SERVICE_NAME = 'mymaster'
    # Redis集群配置信息
    # redis 集群
    REDIS_CLUSTER = [
        {'host': '127.0.0.1', 'port': '7000'},
        {'host': '127.0.0.1', 'port': '7001'},
        {'host': '127.0.0.1', 'port': '7002'},
    ]
    # Redis限流服务配置信息

    # 数据库映射配置信息
    # flask-sqlalchemy使用的参数
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:mysql@127.0.0.1/toutiao'  # 数据库
    SQLALCHEMY_BINDS = {
        'bj-m1': 'mysql://root:mysql@127.0.0.1:3306/toutiao',
        'bj-s1': 'mysql://root:mysql@127.0.0.1:8306/toutiao',
        'masters': ['bj-m1'],
        'slaves': ['bj-s1'],
        'default': 'bj-m1'
    }
    # 追踪数据的修改信号，不设置会报警告，False不追踪可以减少内存消耗
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 显示生成的SQL语句
    SQLALCHEMY_ECHO = True

    # Snowflake ID Worker 参数
    DATACENTER_ID = 0
    WORKER_ID = 0
    SEQUENCE = 0
