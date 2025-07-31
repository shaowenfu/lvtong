# -*- coding: utf-8 -*-
"""
应用初始化模块
- 创建Flask应用实例
- 加载配置
- 注册各个蓝图（路由模块）
"""

from flask import Flask
from .config import Config
from .extensions import cors, mongo
from .routes import register_blueprints

def create_app():
    """
    创建并配置Flask应用
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # 初始化扩展
    cors.init_app(app, resources={
        r"/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    mongo.init_app(app)

    # 注册蓝图
    register_blueprints(app)

    return app

# TODO: 后续可在此添加更多初始化逻辑，如日志、错误处理等
