from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)

# 配置CORS，允许所有域名访问
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# 基础路由
@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'message': 'Flask API Server is running!',
        'status': 'success',
        'version': '1.0.0'
    })

# 健康检查接口
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'message': 'API server is running normally'
    })

# 示例API接口 - 获取用户信息
@app.route('/api/users', methods=['GET'])
def get_users():
    # 模拟用户数据
    users = [
        {'id': 1, 'name': '张三', 'email': 'zhangsan@example.com'},
        {'id': 2, 'name': '李四', 'email': 'lisi@example.com'},
        {'id': 3, 'name': '王五', 'email': 'wangwu@example.com'}
    ]
    return jsonify({
        'status': 'success',
        'data': users,
        'count': len(users)
    })

# 示例API接口 - 创建用户
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({
            'status': 'error',
            'message': '缺少必要参数：name 和 email'
        }), 400
    
    # 模拟创建用户
    new_user = {
        'id': 4,  # 实际项目中应该是数据库生成的ID
        'name': data['name'],
        'email': data['email']
    }
    
    return jsonify({
        'status': 'success',
        'message': '用户创建成功',
        'data': new_user
    }), 201

# 示例API接口 - 获取单个用户
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    # 模拟根据ID查找用户
    users = {
        1: {'id': 1, 'name': '张三', 'email': 'zhangsan@example.com'},
        2: {'id': 2, 'name': '李四', 'email': 'lisi@example.com'},
        3: {'id': 3, 'name': '王五', 'email': 'wangwu@example.com'}
    }
    
    user = users.get(user_id)
    if not user:
        return jsonify({
            'status': 'error',
            'message': '用户不存在'
        }), 404
    
    return jsonify({
        'status': 'success',
        'data': user
    })

# 错误处理
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'status': 'error',
        'message': '接口不存在'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'status': 'error',
        'message': '服务器内部错误'
    }), 500

if __name__ == '__main__':
    # 从环境变量获取配置，默认值适用于开发环境
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(host=host, port=port, debug=debug)