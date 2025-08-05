#!/bin/bash

# Dozzle 日志查看器部署脚本
# 用于快速部署和更新 Dozzle 服务

set -e  # 遇到错误立即退出

echo "🚀 开始部署 Dozzle 日志查看器..."

# 检查是否在正确的目录
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 检查 Docker 和 Docker Compose 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ 错误: Docker 未安装"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ 错误: Docker Compose 未安装"
    exit 1
fi

echo "📋 检查当前服务状态..."
docker-compose ps

echo "🔄 停止现有服务..."
docker-compose down

echo "🏗️  重新构建并启动服务..."
docker-compose up -d --build

echo "⏳ 等待服务启动..."
sleep 10

echo "🔍 检查服务状态..."
docker-compose ps

echo "🩺 检查 Nginx 配置..."
if docker-compose exec -T nginx nginx -t; then
    echo "✅ Nginx 配置检查通过"
    echo "🔄 重新加载 Nginx 配置..."
    docker-compose exec -T nginx nginx -s reload
else
    echo "❌ Nginx 配置检查失败"
    exit 1
fi

echo "🔍 检查 Dozzle 服务健康状态..."
for i in {1..30}; do
    if docker-compose exec -T dozzle wget --quiet --tries=1 --spider http://localhost:8080; then
        echo "✅ Dozzle 服务运行正常"
        break
    else
        echo "⏳ 等待 Dozzle 服务启动... ($i/30)"
        sleep 2
    fi
    
    if [ $i -eq 30 ]; then
        echo "❌ Dozzle 服务启动超时"
        echo "📋 查看 Dozzle 日志:"
        docker-compose logs dozzle
        exit 1
    fi
done

echo ""
echo "🎉 Dozzle 部署完成!"
echo ""
echo "📊 访问方式:"
echo "  • HTTPS: https://lvtong.sherwenfu.com/logs"
echo "  • HTTP:  http://47.108.89.109/logs"
echo ""
echo "📋 监控的容器:"
echo "  • mongodb (MongoDB 数据库)"
echo "  • flask-api (Flask 后端服务)"
echo "  • nginx-proxy (Nginx 反向代理)"
echo "  • mongo-express (MongoDB 管理界面)"
echo ""
echo "🔧 管理命令:"
echo "  • 查看所有服务状态: docker-compose ps"
echo "  • 查看 Dozzle 日志: docker-compose logs -f dozzle"
echo "  • 重启 Dozzle: docker-compose restart dozzle"
echo "  • 停止所有服务: docker-compose down"
echo ""
echo "📖 详细文档请查看: DOZZLE_SETUP.md"
echo "✨ 部署完成!"