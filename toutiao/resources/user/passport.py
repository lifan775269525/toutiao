# -*-Coding:UTF-8 -*-
"""
程序：
版本：1.0
作者：鬼义虎神
日期：
功能：
    1. 
"""
import time
from datetime import datetime, timedelta
from flask_restful import Resource, current_app, reqparse, inputs

from models import db
from utils import parser
from utils.jwt_util import generate_jwt
from models.user import User, UserProfile
from utils.decorators import set_db_to_write, set_db_to_read


# 用户视图类
class AuthorizationResource(Resource):
    method_decorators = {
        'post': [set_db_to_write],
        'put': [set_db_to_read]
    }

    def _generate_tokens(self, user_id, with_refresh_token=True):
        """
        生成token有效期2小时 和refresh_token有效期14天
        :param user_id: 用户id
        :return: token, refresh_token
        """
        # generate_jwt(payload, expiry, secret=None)
        # 生成当前时间
        now = datetime.utcnow()
        exp = now + timedelta(hours=current_app.config.get('JWT_EXPIRY_HOURS'))
        # 业务token
        token = generate_jwt({'user_id': user_id, 'is_refresh': False}, exp, secret=None)
        # 判断是否生成刷新token
        refresh_token = None
        if with_refresh_token:
            # 生成刷新token
            exp = now + timedelta(days=current_app.config.get('JWT_REFRESH_DAYS'))
            refresh_token = generate_jwt({'user_id': user_id, 'is_refresh': True}, exp, secret=None)

        # 返回两个token
        return token, refresh_token

    def get(self):
        print('进入用户认证模块')
        return '进入用户认证模块'

    def post(self):
        """登录、注册创建token（JWT）"""
        """接收参数、校验参数"""
        # 验证手机号、验证码
        rep = reqparse.RequestParser()
        rep.add_argument('mobile', required=True, type=parser.moblie, location='json')
        rep.add_argument('code', required=True, type=inputs.regex(r'^\d{6}$'), location='json')
        # 启用验证并获取校验后的参数
        args = rep.parse_args()
        mobile = args.mobile
        code = args.code
        print('获取的手机号为：', mobile)
        print('获取的验证码为：', code)

        """数据处理"""
        # 根据mobile组合成key，去redis中取code
        key = f"app:code:{mobile}"
        try:
            # 先从主中获取，主里面没有再去从里尝试获取
            real_code = current_app.redis_master.get(key)
        except ConnectionError as err:
            current_app.logger(err)
            print(err)
            print('主Redis中并没有找到code，开始尝试从从Redis中获取。')
            real_code = current_app.redis_slave.get(key)

        # 不管有没有，先删除code，保证验证码只能使用一次
        try:
            current_app.redis_master.delete(key)
        except ConnectionError as err:
            current_app.logger(err)
            print('因为Redis中只有主可以进行写操作，所以可能从从中删除', err)

        # 如果Code不正确，直接返回错误信息
        if (not real_code) or (code != real_code.decode()):
            return {'message': '验证码无效'}, 400

        # 正确的话开始判断用户是否存在
        user = User.query.filter(User.mobile == mobile).first()
        # 如果用户不存在注册用户
        if not user:
            user_id = current_app.id_worker.get_id()
            user = User(id=user_id, mobile=mobile, name=mobile, last_login=datetime.now())
            db.session.add(user)
            user_profile = UserProfile(id=user_id)
            db.session.add(user_profile)
            db.session.commit()
        else:
            if user.status == User.STATUS.DISABLE:
                print('用户已经被禁用')
                return {'message': '用户已经被禁用'}, 403

        print('用户正常，开始获取JWT。')
        token, refresh_token = self._generate_tokens(user.id)
        print('token:', token)
        print('refresh_token:', refresh_token)

        """返回响应"""
        return {'token': token, 'refresh_token': refresh_token}, 201
