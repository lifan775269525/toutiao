# -*-Coding:UTF-8 -*-
"""
程序：
版本：1.0
作者：鬼义虎神
日期：
功能：
    1. 
"""
from json import dumps
from flask_restful.utils import PY3
from flask import make_response, current_app, request


def output_json(data, code, headers=None):
    """Makes a Flask response with a JSON encoded body"""
    # 验证返回的状态码，如果返是400
    if str(code) == '400':
        # 打印警告日志，请求头、请求体参数、返回信息
        current_app.logger.warn(request.headers)
        current_app.logger.warn(request.data)
        current_app.logger.warn(str(data))

    # 封装返回json的格式
    # 为什么要检验message呢，因为flask报错默认返回key为message的错误信息
    if 'message' not in data:
        data = {
            'message': 'OK',
            'data': data
        }

    settings = current_app.config.get('RESTFUL_JSON', {})

    # If we're in debug mode, and the indent is not set, we set it to a
    # reasonable value here.  Note that this won't override any existing value
    # that was set.  We also set the "sort_keys" value.
    if current_app.debug:
        settings.setdefault('indent', 4)
        settings.setdefault('sort_keys', not PY3)

    # always end the json dumps with a new line
    # see https://github.com/mitsuhiko/flask/pull/1262
    dumped = dumps(data, **settings) + "\n"

    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp
