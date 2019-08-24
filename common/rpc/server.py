# -*-Coding:UTF-8 -*-
"""
程序：服务器
版本：1.0
作者：鬼义虎神
日期：
功能：
    1. 
"""
import time
import grpc
from concurrent.futures import ThreadPoolExecutor

import reco_pb2
import reco_pb2_grpc


# 用来创建rpc服务器
# 定义服务器类
class UserRecommendsServicer(object):
    """相当于Python中定义一个类
    """

    def user_recommends(self, request, context):
        # 用户推荐
        # 获取请求信息
        user_id = request.user_id
        channel_id = request.channel_id
        article_num = request.article_num
        time_stamp = request.time_stamp
        # 此处代码为伪推荐，后续系统推荐课程中，可以补全此处代码
        resp = reco_pb2.ArticleResponse()
        resp.exposure = 'exposure data'
        resp.time_stamp = round(time.time() * 1000)
        content = []
        for i in range(article_num):
            article = reco_pb2.Article()
            article.article_id = i
            article.track.click = 'click data {}'.format(i + 1)
            article.track.collect = 'collect data {}'.format(i + 1)
            article.track.share = 'share data {}'.format(i + 1)
            article.track.read = 'read data {}'.format(i + 1)
            content.append(article)
        resp.recommends.extend(content)
        # 返回响应
        return resp


# 创建RPC服务器
def server():
    # 1. 创建rpc服务器，必须指定线程池，默认10个线程
    server = grpc.server(thread_pool=ThreadPoolExecutor(max_workers=10))
    # 2. 给服务器添加服务方法
    reco_pb2_grpc.add_UserRecommendsServicer_to_server(UserRecommendsServicer(), server)
    # 3. 绑定host和port
    server.add_insecure_port('127.0.0.1:8888')
    # 4. 启动服务器，非阻塞服务器，执行完就结束
    server.start()
    # 所以我们手动让整个程序阻塞
    while True:
        time.sleep(10)


if __name__ == '__main__':
    server()
