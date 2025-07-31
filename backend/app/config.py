# -*- coding: utf-8 -*-
"""
配置模块
- 管理Flask应用的所有配置
- 支持通过环境变量设置敏感信息
"""

import os

class Config(object):
    """基础配置类"""
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/lvtong")
    MONGO_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/lvtong")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_azure_key")
    OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://your-azure-endpoint.openai.azure.com/")
    OPENAI_API_VERSION = os.getenv("OPENAI_API_VERSION", "2023-05-15")
    # TODO: 可在此添加更多配置项，如日志、缓存、第三方服务等

# TODO: 如需多环境（开发/生产）配置，可继承Config类扩展
