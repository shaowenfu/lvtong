#!/bin/bash

# 部署脚本 - LvTong 项目
# 使用方法: ./deploy.sh [start|stop|restart|logs|status]

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查 .env 文件
check_env_file() {
    if [ ! -f ".env" ]; then
        log_warning ".env 文件不存在，正在从模板创建..."
        if [ -f ".env.production" ]; then
            cp .env.production .env
            log_warning "请编辑 .env 文件，填入正确的配置值"
            log_warning "特别是 OPENAI_API_KEY 等敏感信息"
        else
            log_error ".env.production 模板文件不存在"
            exit 1
        fi
    fi
}

# 启动服务
start_services() {
    log_info "启动 LvTong 服务..."
    check_env_file
    docker-compose up -d
    log_success "服务启动完成"
    log_info "等待服务健康检查..."
    sleep 10
    docker-compose ps
}

# 停止服务
stop_services() {
    log_info "停止 LvTong 服务..."
    docker-compose down
    log_success "服务已停止"
}

# 重启服务
restart_services() {
    log_info "重启 LvTong 服务..."
    stop_services
    start_services
}

# 查看日志
view_logs() {
    log_info "查看服务日志..."
    docker-compose logs -f
}

# 查看状态
check_status() {
    log_info "检查服务状态..."
    docker-compose ps
    echo ""
    log_info "健康检查状态:"
    docker-compose exec backend curl -f http://localhost:5000/health 2>/dev/null && log_success "Backend 健康" || log_error "Backend 不健康"
    docker-compose exec mongodb mongosh --eval "db.adminCommand('ping')" --quiet 2>/dev/null && log_success "MongoDB 健康" || log_error "MongoDB 不健康"
}

# 主函数
main() {
    case "$1" in
        start)
            start_services
            ;;
        stop)
            stop_services
            ;;
        restart)
            restart_services
            ;;
        logs)
            view_logs
            ;;
        status)
            check_status
            ;;
        *)
            echo "使用方法: $0 {start|stop|restart|logs|status}"
            echo ""
            echo "命令说明:"
            echo "  start   - 启动所有服务"
            echo "  stop    - 停止所有服务"
            echo "  restart - 重启所有服务"
            echo "  logs    - 查看实时日志"
            echo "  status  - 检查服务状态"
            exit 1
            ;;
    esac
}

main "$@"