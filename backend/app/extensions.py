# -*- coding: utf-8 -*-
"""
Flask扩展初始化模块
- 统一管理所有Flask扩展实例
- 避免循环引用
"""

from flask_pymongo import PyMongo
from flask_cors import CORS

# 初始化MongoDB扩展
mongo = PyMongo()
# 初始化CORS扩展
cors = CORS()

# TODO: 如需添加更多扩展（如JWT、缓存等），可在此统一管理
