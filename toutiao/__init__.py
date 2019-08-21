# -*-Coding:UTF-8 -*-
"""
程序：创建flask的对象
版本：1.0
作者：鬼义虎神
日期：
功能：
    1. 利用工厂函数创建flask的app对象
"""
from flask import Flask


# 创建原始的Flask对象的app
def create_flask_app(Config, enable_config_file=False):
    """
    创建最原始的Flask对象的app
    :param config: 配置文件类
    :param enable_config_file: 是否允许环境变量中的配置文件覆盖已加载的配置信息，默认False
    :return: 原始的Flask框架的app
    """
    app = Flask(__name__)
    # 加载配置文件类
    app.config.from_object(Config)
    # 是否允许运行环境中的配置文件覆盖已加载配置
    if enable_config_file:
        # 导入项目存放常量的文件
        from utils import constants
        # 参数1：配置文件环境变量名，参数2：报错不显示配置文件位置
        app.config.from_envvar(constants.GLOBAL_SETTING_ENV_NAME, silent=True)

    return app


def create_app(Config, enable_config_file=False):
    """
    创建应用的工厂函数
    :param config: 配置信息类
    :param enable_config_file: 是否允许环境变量中的配置文件覆盖已加载的配置信息
    :return: 应用对象
    """
    app = create_flask_app(Config, enable_config_file)
    """项目运行需要的配置"""
    # 配置日志
    from utils.logging import create_logger
    create_logger(app)

    # 配置redis哨兵
    from redis.sentinel import Sentinel
    _sentinel = Sentinel(app.config.get('REDIS_SENTINELS'))
    # 根据哨兵设置主、从服务
    app.redis_master = _sentinel.master_for(app.config['REDIS_SENTINEL_SERVICE_NAME'])
    app.redis_slave = _sentinel.slave_for(app.config['REDIS_SENTINEL_SERVICE_NAME'])
    # Redis集群
    from rediscluster import StrictRedisCluster
    app.redis_cluster = StrictRedisCluster(startup_nodes=app.config['REDIS_CLUSTER'])

    # MySQL数据库连接初始化
    from models import db
    db.init_app(app)

    # 创建Snowflake ID worker--雪花算法
    from utils.snowflake.id_worker import IdWorker
    app.id_worker = IdWorker(app.config['DATACENTER_ID'],
                             app.config['WORKER_ID'],
                             app.config['SEQUENCE'])

    """添加请求钩子"""
    from utils.middlewares import jwt_authentication
    app.before_request(jwt_authentication)

    """注册蓝图"""
    # 用户蓝图
    from toutiao.resources.user import user_bp
    app.register_blueprint(user_bp)

    return app
