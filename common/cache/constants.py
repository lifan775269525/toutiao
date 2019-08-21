# -*-Coding:UTF-8 -*-
"""
程序：各种缓存的过期时间
版本：1.0
作者：鬼义虎神
日期：2019年8月21日
功能：
    1. 因为查询不同的数据需要不同有效期，所以封装成一个类
"""
import random
from datetime import timedelta


# 基础的有效期类
class BaseCacheTTL(object):
    # 基础过期时间
    TTL = 5 * 50
    # 偏差过期时间，为了防止缓存雪崩问题
    TIME_DELTA = 0

    @classmethod
    def get_exp(cls):
        exp = cls.TTL + random.randint(1, cls.TIME_DELTA)
        return exp


class UserCacheTTL(BaseCacheTTL):
    TTL = 10 * 50


class UserProfileCacheTTL(BaseCacheTTL):
    TTL = 25 * 50


class UserNotExistCacheTTL(BaseCacheTTL):
    TTL = 15 * 50
