# -*-Coding:UTF-8 -*-
"""
程序：
版本：1.0
作者：鬼义虎神
日期：2019年8月24日
功能：
    1. 
"""
import time

import grpc

import reco_pb2
import reco_pb2_grpc


# 喂养数据，根据构建的请求，发送请求，获取相应
def feed_articles(stub):
    req = reco_pb2.UserRequest()
    req.user_id = '1'
    req.channel_id = 2
    req.article_num = 5
    req.time_stamp = round(time.time() * 1000)
    # 我们在proto中定义的方法，根据请求获取相应
    resp = stub.user_recommends(req)
    print('resp = {}'.format(resp))


def run():
    # 连接服务器
    with grpc.insecure_channel('127.0.0.1:8888') as channel:
        # 创建媒婆对象，用于解析、打包、序列化数据
        stub = reco_pb2_grpc.UserRecommendsStub(channel)
        feed_articles(stub)


if __name__ == '__main__':
    run()
