# -*-Coding:UTF-8 -*-
"""
程序：修正Redis和MySQL数据的一致性，把统计数据更新到redis中；
版本：1.0
作者：鬼义虎神
日期：2019年8月23日
功能：
    1. 查询MySQL-->删除redis-->更新redis
    由定时任务的调度器模块执行这个模块
步骤：
    查询MySQL
    删除Redis
    更新Redis
"""
from flask import current_app

from cache import statistic


def __fix(tools_class):
    result = tools_class.db_query()
    tools_class.reset(result)


# 定时任务的任务函数
def fix_process(flask_app):
    """更新Redis，使其和MySQL中数据一致"""
    # 为什么需要传入app呢？因为db_query需要使用查询数据库，这个必须开启上下文
    with flask_app.app_context():
        # 用户发布文章
        __fix(statistic.UserArticleCache)
        # 用户关注数
        __fix(statistic.UserFollowingCache)

        """会发现代码重复，进一步封装"""
        # 用户发布文章数
        # result = statistic.UserArticleCache.db_query()
        # statistic.UserArticleCache.reset(result)

        # 用户关注数
        # result = statistic.UserFollowingCache.db_query()
        # statistic.UserFollowingCache.reset(result)
