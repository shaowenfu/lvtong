# -*- coding: utf-8 -*-
"""
路由注册模块
- 统一注册所有蓝图（功能模块的路由）
"""

from .report import report_bp
from .chat import chat_bp

def register_blueprints(app):
    """
    注册所有蓝图到Flask应用
    """
    app.register_blueprint(report_bp, url_prefix="/api/report")
    app.register_blueprint(chat_bp, url_prefix="/api/chat")
    # TODO: 如需添加新功能模块，在此注册对应蓝图
