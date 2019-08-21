# -*-Coding:UTF-8 -*-
"""
程序：缓存工具类
版本：1.0
作者：鬼义虎神
日期：2019年8月21日
功能：
    1. 解决MySQL数据库的负载过重问题，结局击穿问题、雪崩问题
    缓存工具类
    查询数据先从redis中查
        有数据
            返回（区分有效数据和无效数据）
        无数据
          才去MySQL中查询
             有数据
                先存到redis，再返回（注意数据雪崩问题）
             无数据
                将其设置成无效数据存入redis中，返回None

    注意：其他缓存工具类只需要基础此类，更高__init__中的key即可
"""
import json
from flask import current_app

from . import constants
from models.user import User


class UserCache(object):
    """用户的缓存数据工具类"""

    def __init__(self, user_id):
        self.key = 'user:{}:profile'.format(user_id)
        self.user_id = user_id

    # 查询对应的数据
    def get(self):
        """查询对应的数据"""
        # 1.连接Redis数据库app.redis_cluster
        redis_client = current_app.redis_cluster
        # 2.根据key，查询redis数据库
        data = redis_client.get(self.key)
        # 3.如果有数据
        if data:
            print('Redis有数据，开始判断是否有效')
            # 3.1进一步判断数据是否为无效数据，-1，缓存击穿
            if data != '-1'.encode():
                # 3.2有效数据，转成字典；返回
                return json.dumps(data)
            else:
                print('无效数据')
                return None
        # 4.否则没数据
        else:
            print('Redis中无数据，开始去MySQL中查询。')
            # 4.1查询mysql
            data = self.search()
            return data

    # 删除对应的数据
    def delete(self):
        """删除对应的数据"""
        redis_client = current_app.redis_cluster
        redis_client.delete(self.key)

    # 判断对应的数据是否存在
    def is_exist(self):
        """判断对应的数据是否存在"""
        # 1.连接Redis数据库app.redis_cluster
        redis_clint = current_app.redis_cluster
        # 2.根据key，查询redis数据库
        data = redis_clint.get(self.key)
        # 3.如果有数据
        if data:
            # 3.1进一步判断数据是否为无效数据，-1，缓存击穿
            if data != '-1'.encode():
                # 3.2有效数据，转成字典；返回
                return True
            else:
                print('无效数据')
                return False
        # 4.否则没数据
        else:
            data = self.search()
            if data:
                return True
            else:
                return False

    # 封装查询数据库的代码
    def search(self):
        """
        查询数据库，如果有数据，判断是否是有效数据
            有效：存入转成json存入redis，最后返回数据
            无效：将-1存入redis，返回None
        """
        redis_client = current_app.redis_cluster
        try:
            user = User.query.get(id=self.user_id)
            # 4.2如果有数据，把查询对象保存字典数据
            # 4.3转成json，存入redis中，缓存雪崩
            user_dict = dict(
                mobile=user.mobile,
                name=user.name,
                photo=user.profile_photo,
                intro=user.introduction,
                cert=user.certificate
            )
            user_json = json.dumps(user_dict)
            print('有对应的数据，将数据存入Redis中，作为缓存。')
            redis_client.setx(self.key, constants.UserCacheTTL.get_exp(), user_json)
            return user_dict
        # 4.4否则没数据，在redis`中存入无效数据-1,缓存击穿
        except Exception as err:
            print('没有对应的数据，在Redis中存入无效数据')
            redis_client.setx(self.key, constants.UserNotExistCacheTTL.get_exp(), -1)
            return None
