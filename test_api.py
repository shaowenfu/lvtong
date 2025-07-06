#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Flask API 测试脚本

这个脚本用于测试 Flask API 服务器的各个接口功能。
使用前请确保服务器已经启动（运行 start_server.bat 或 docker-compose up）。

使用方法：
    python test_api.py
"""

import requests
import json
import time
from typing import Dict, Any

# API 基础配置
BASE_URL = "http://localhost"
HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Flask-API-Test-Script/1.0"
}

def print_separator(title: str = ""):
    """打印分隔线"""
    print("\n" + "=" * 60)
    if title:
        print(f" {title} ")
        print("=" * 60)

def print_response(response: requests.Response, test_name: str):
    """格式化打印响应结果"""
    print(f"\n🧪 测试: {test_name}")
    print(f"📡 请求: {response.request.method} {response.url}")
    print(f"📊 状态码: {response.status_code}")
    
    try:
        response_data = response.json()
        print(f"📄 响应数据:")
        print(json.dumps(response_data, ensure_ascii=False, indent=2))
    except json.JSONDecodeError:
        print(f"📄 响应内容: {response.text}")
    
    if response.status_code >= 200 and response.status_code < 300:
        print("✅ 测试通过")
    else:
        print("❌ 测试失败")
    
    print("-" * 40)

def test_health_check():
    """测试健康检查接口"""
    try:
        response = requests.get(f"{BASE_URL}/health", headers=HEADERS, timeout=10)
        print_response(response, "健康检查")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"❌ 健康检查失败: {e}")
        return False

def test_home_page():
    """测试主页接口"""
    try:
        response = requests.get(f"{BASE_URL}/", headers=HEADERS, timeout=10)
        print_response(response, "主页")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"❌ 主页测试失败: {e}")
        return False

def test_get_users():
    """测试获取用户列表"""
    try:
        response = requests.get(f"{BASE_URL}/api/users", headers=HEADERS, timeout=10)
        print_response(response, "获取用户列表")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"❌ 获取用户列表失败: {e}")
        return False

def test_create_user():
    """测试创建用户"""
    user_data = {
        "name": "测试用户",
        "email": "test@example.com"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/users", 
            headers=HEADERS, 
            json=user_data, 
            timeout=10
        )
        print_response(response, "创建用户")
        return response.status_code == 201
    except requests.exceptions.RequestException as e:
        print(f"❌ 创建用户失败: {e}")
        return False

def test_get_single_user():
    """测试获取单个用户"""
    user_id = 1
    try:
        response = requests.get(f"{BASE_URL}/api/users/{user_id}", headers=HEADERS, timeout=10)
        print_response(response, f"获取用户 ID: {user_id}")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"❌ 获取单个用户失败: {e}")
        return False

def test_get_nonexistent_user():
    """测试获取不存在的用户"""
    user_id = 999
    try:
        response = requests.get(f"{BASE_URL}/api/users/{user_id}", headers=HEADERS, timeout=10)
        print_response(response, f"获取不存在的用户 ID: {user_id}")
        return response.status_code == 404
    except requests.exceptions.RequestException as e:
        print(f"❌ 测试不存在用户失败: {e}")
        return False

def test_create_user_invalid_data():
    """测试创建用户 - 无效数据"""
    invalid_data = {
        "name": "测试用户"  # 缺少 email 字段
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/users", 
            headers=HEADERS, 
            json=invalid_data, 
            timeout=10
        )
        print_response(response, "创建用户 - 无效数据")
        return response.status_code == 400
    except requests.exceptions.RequestException as e:
        print(f"❌ 测试无效数据失败: {e}")
        return False

def test_nonexistent_endpoint():
    """测试不存在的接口"""
    try:
        response = requests.get(f"{BASE_URL}/api/nonexistent", headers=HEADERS, timeout=10)
        print_response(response, "不存在的接口")
        return response.status_code == 404
    except requests.exceptions.RequestException as e:
        print(f"❌ 测试不存在接口失败: {e}")
        return False

def test_cors():
    """测试 CORS 支持"""
    cors_headers = {
        **HEADERS,
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "Content-Type"
    }
    
    try:
        # 发送 OPTIONS 预检请求
        response = requests.options(f"{BASE_URL}/api/users", headers=cors_headers, timeout=10)
        print_response(response, "CORS 预检请求")
        
        # 检查 CORS 头部
        cors_origin = response.headers.get('Access-Control-Allow-Origin')
        cors_methods = response.headers.get('Access-Control-Allow-Methods')
        
        print(f"🔍 CORS 检查:")
        print(f"   Allow-Origin: {cors_origin}")
        print(f"   Allow-Methods: {cors_methods}")
        
        return response.status_code in [200, 204] and cors_origin is not None
    except requests.exceptions.RequestException as e:
        print(f"❌ CORS 测试失败: {e}")
        return False

def run_performance_test():
    """简单的性能测试"""
    print_separator("性能测试")
    
    test_count = 10
    start_time = time.time()
    success_count = 0
    
    print(f"🚀 执行 {test_count} 次健康检查请求...")
    
    for i in range(test_count):
        try:
            response = requests.get(f"{BASE_URL}/health", headers=HEADERS, timeout=5)
            if response.status_code == 200:
                success_count += 1
            print(f"请求 {i+1}: {response.status_code} ({response.elapsed.total_seconds():.3f}s)")
        except requests.exceptions.RequestException as e:
            print(f"请求 {i+1}: 失败 - {e}")
    
    end_time = time.time()
    total_time = end_time - start_time
    avg_time = total_time / test_count
    success_rate = (success_count / test_count) * 100
    
    print(f"\n📊 性能测试结果:")
    print(f"   总请求数: {test_count}")
    print(f"   成功请求: {success_count}")
    print(f"   成功率: {success_rate:.1f}%")
    print(f"   总耗时: {total_time:.3f}s")
    print(f"   平均响应时间: {avg_time:.3f}s")
    print(f"   QPS: {test_count/total_time:.1f}")

def main():
    """主测试函数"""
    print_separator("Flask API 服务器测试")
    print(f"🎯 测试目标: {BASE_URL}")
    print(f"⏰ 测试时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 测试用例列表
    test_cases = [
        ("基础功能测试", [
            ("健康检查", test_health_check),
            ("主页", test_home_page),
            ("获取用户列表", test_get_users),
            ("获取单个用户", test_get_single_user),
            ("创建用户", test_create_user),
        ]),
        ("错误处理测试", [
            ("获取不存在的用户", test_get_nonexistent_user),
            ("创建用户 - 无效数据", test_create_user_invalid_data),
            ("不存在的接口", test_nonexistent_endpoint),
        ]),
        ("跨域支持测试", [
            ("CORS 支持", test_cors),
        ])
    ]
    
    total_tests = 0
    passed_tests = 0
    
    # 执行测试用例
    for category, tests in test_cases:
        print_separator(category)
        
        for test_name, test_func in tests:
            total_tests += 1
            if test_func():
                passed_tests += 1
            time.sleep(0.5)  # 避免请求过于频繁
    
    # 执行性能测试
    run_performance_test()
    
    # 测试总结
    print_separator("测试总结")
    success_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"📈 测试统计:")
    print(f"   总测试数: {total_tests}")
    print(f"   通过测试: {passed_tests}")
    print(f"   失败测试: {total_tests - passed_tests}")
    print(f"   成功率: {success_rate:.1f}%")
    
    if success_rate >= 80:
        print(f"\n🎉 测试结果: 优秀! API 服务器运行正常")
    elif success_rate >= 60:
        print(f"\n⚠️  测试结果: 良好，但有部分问题需要关注")
    else:
        print(f"\n❌ 测试结果: 需要检查，存在较多问题")
    
    print(f"\n💡 提示:")
    print(f"   - 如果测试失败，请检查服务器是否正在运行")
    print(f"   - 运行 'docker-compose ps' 查看服务状态")
    print(f"   - 运行 'docker-compose logs' 查看详细日志")
    
    print_separator()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⏹️  测试被用户中断")
    except Exception as e:
        print(f"\n\n💥 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()