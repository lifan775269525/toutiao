# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

import reco_pb2 as reco__pb2


class UserRecommendsStub(object):
  """相当于Python中定义一个类
  """

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.user_recommends = channel.unary_unary(
        '/UserRecommends/user_recommends',
        request_serializer=reco__pb2.UserRequest.SerializeToString,
        response_deserializer=reco__pb2.ArticleResponse.FromString,
        )


class UserRecommendsServicer(object):
  """相当于Python中定义一个类
  """

  def user_recommends(self, request, context):
    """定义一个函数，接收请求参数，返回相应数据
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_UserRecommendsServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'user_recommends': grpc.unary_unary_rpc_method_handler(
          servicer.user_recommends,
          request_deserializer=reco__pb2.UserRequest.FromString,
          response_serializer=reco__pb2.ArticleResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'UserRecommends', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
