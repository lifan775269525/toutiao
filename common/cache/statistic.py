# -*-Coding:UTF-8 -*-
"""
程序：
版本：1.0
作者：鬼义虎神
日期：2019年8月22日
需求：使用Redis主从获取统计数据
功能：
查询用户发布的文章数量
SQL：
select user_id,count(article_id) from news_article_basic where status=2 group by user_id;
ORM：
db.session.query(Article.user_id, func.count(Article.article_id)).filter(Article.status=2).group_by(Article.user_id).all()
数据统计实现步骤：
    1. 操作redis主从获取指定用户的文章数（score）
    2. 如果未取到，从从redis中获取
    3. 获取数据时二进制值的：可以这样转换int(b'100')
    4. 获取没有就返回0
"""
from sqlalchemy import func
from redis import RedisError
from flask_restful import current_app

from models import db
from models.news import Article
from models.user import User, Relation


class CountStorageBase(object):
    """每一个继承这个类的都需要重写key和db_query"""
    key = ''

    # 获取文章数
    @classmethod
    def get(cls, user_id):
        try:
            # 1. 操作redis主从获取指定用户的文章数（score）
            article_count = current_app.redis_master.zscore(cls.key, user_id)
        except RedisError as err:
            # 2. 如果未取到，从从redis中获取
            current_app.logger.error(err)
            print('主Redis中没有数据，开始从从Redis中读文章数据！')
            article_count = current_app.redis_slave(cls.key, user_id)

        if current_app:
            # 3. 获取数据时二进制值的：可以这样转换int(b'100')
            return int(article_count)
        else:
            # 4. 获取没有就返回0
            return 0

        pass

    # 文章数自增
    @classmethod
    def incr(cls, user_id, increment=1):
        try:
            current_app.redis_master.zincrby(cls.key, increment, user_id)
        except RedisError as err:
            current_app.logger.error(err)
            print('XXX自增出错！', err)

    # 从MySQL中获取真实的数据
    @staticmethod
    def db_query():
        pass

    # 文章数重置
    @classmethod
    def reset(cls, result_list):
        try:
            current_app.redis_master.delete(cls.key)
        except RedisError as err:
            current_app.logger.error(err)
            print('根据key删除用户原始的XXX异常', err)

        # 更新Redis
        # user_article_list 的样式[(1, 2), (3, 40), (5, 66), ...]
        # 为了避免频繁的连接，我们可以使用Redis管道，当然也可以直接把格式构造成[2,1, 40,3, 66,5,...]插入(数量做权重，id做小key)
        data = []
        for user_id, article_count in result_list:
            data.append(article_count)
            data.append(user_id)
        try:
            # 据说拆包只有2.X的Redis版本可以用，3.X的不行
            current_app.redis_master.zadd(cls.key, *data)
        except RedisError as err:
            current_app.logger.error(err)
            print('更新异常', err)


class UserArticleCache(CountStorageBase):
    key = 'count:user:arts'

    # 从MySQL中获取真实的数据
    @staticmethod
    def db_query():
        user_article_list = []
        try:
            user_article_list = db.session.query(Article.user_id, func.count(Article.id)).filter(
                Article.status == Article.STATUS.APPROVED).group_by(Article.user_id).all()
        except Exception as err:
            current_app.logger.error(err)
            print('查询MySQL：用户审核通过的文章数异常', err)

        return user_article_list


# 用户关注是数（为实现）
class UserFollowingCache(CountStorageBase):
    key = 'count:user:follow'

    # 从MySQL中获取真实的数据
    @staticmethod
    def db_query():
        user_follow_list = list()
        try:
            user_follow_list = db.session.query(Relation.user_id, func.count(Relation.target_user_id)).filter(
                Relation.relation == Relation.RELATION.FOLLOW).group_by(Relation.user_id).all()
        except Exception as err:
            current_app.logger.error(err)
            print('查询MySQL：用户关注数异常', err)

        return user_follow_list
