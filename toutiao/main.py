import os
import sys

# 设置命令行启动
# 项目根目录：当前文件的上级目录的上级目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(BASE_DIR)
# 将根目录下的common文件添加到python的系统目录下
sys.path.insert(0, os.path.join(BASE_DIR, 'common'))

from flask import jsonify

from . import create_app
from settings.default import DefaultConfig

# 根据工厂函数获取Flask框架的app应用
app = create_app(DefaultConfig, True)


@app.route('/')
def route_map():
    """主视图，返回所有视图网址"""
    # 获取整个Flask框架的路由映射信息--的迭代对象
    rules_iterator = app.url_map.iter_rules()
    # 变形的字典生成器，{端点：路由}，只要端点不是static的和route_map的
    url_dict = {rule.endpoint: rule.rule for rule in rules_iterator if rule.endpoint not in ('route_map', 'static')}
    # 返回json
    return jsonify(url_dict)
