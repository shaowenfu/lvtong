# -*- coding: utf-8 -*-
"""
主应用入口文件
- 使用应用工厂模式创建Flask应用
- 集成app目录中的模块化架构
"""

from dotenv import load_dotenv
import os
import sys

# 确保当前目录在Python路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 加载环境变量
load_dotenv()

from flask import jsonify
from app import create_app

# 创建Flask应用实例
app = create_app()

# 添加根路由和健康检查
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Flask API Server is running!',
        'status': 'success',
        'version': '1.0.0'
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'API server is running normally'
    })

# 全局错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': 'API endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # 从环境变量获取配置，默认值适用于开发环境
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)