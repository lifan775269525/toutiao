# -*-Coding:UTF-8 -*-
"""
程序：ORM映射初始化
版本：1.0
作者：鬼义虎神
日期：
功能：
    1. 
"""
# from flask_sqlalchemy import SQLAlchemy
from .db_routing.routing_sqlalchemy import RoutingSQLAlchemy


db = RoutingSQLAlchemy()
