# Flask API 服务器项目

这是一个基于Flask的API服务器项目，专为阿里云ECS服务器部署设计。使用Docker容器化Flask应用，配合系统Nginx作为反向代理，提供高性能的API服务。

## 项目架构

```
Flutter App (iOS/Android/Web)    <-- (外网) -->    公网API域名 (e.g., api.yourdomain.com)
        |
        |   (DNS解析)
        V
阿里云ECS服务器 (公网IP)
        |
        |   (防火墙开放80/443端口)
        V
[   系统Nginx反向代理   ]     (处理SSL, 负载均衡)
        |
        V
[   Flask API容器 (端口5000)   ]
```

## 项目结构

```
Lvtong/
├── README.md                           # 项目说明文档
├── docker-compose.yml                 # Docker编排配置
├── backend/                            # Flask应用源码目录
│   ├── app.py                         # Flask主应用文件
│   ├── requirements.txt               # Python依赖
│   └── Dockerfile                     # 后端Docker构建文件
├── nginx/                              # Nginx配置模板目录
│   └── nginx.conf                     # Nginx配置模板
└── test_api.py                        # API测试脚本
```

## 部署环境要求

### 服务器要求

- 阿里云ECS服务器
- Ubuntu 18.04+ 或 CentOS 7+
- 至少2GB内存，1核CPU
- 已开放80和443端口（安全组配置）

### 软件要求

- Docker 20.10+
- Docker Compose 2.0+
- Nginx (系统安装)
- 域名（可选，推荐用于生产环境）

## 快速部署指南

### 1. 服务器环境准备

```bash
# 更新系统
sudo apt update && sudo apt upgrade -y

# 安装Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 安装Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# 安装Nginx
sudo apt install nginx -y
```

### 2. 项目部署

```bash
# 上传项目到服务器
scp -r ./Lvtong root@your-server-ip:/root/workspace/

# 连接服务器
ssh root@your-server-ip

# 进入项目目录
cd /root/workspace/lvtong

# 构建并启动后端服务
docker-compose build backend
docker-compose up -d backend

# 验证后端服务
docker-compose ps
curl http://localhost:5000/health
```

### 3. 配置系统Nginx

```bash
# 创建Nginx站点配置
sudo nano /etc/nginx/sites-available/lvtong-api
```

添加以下配置内容：

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 替换为您的域名或使用 _ 匹配所有
    
    # 安全头设置
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
    
    # 启用gzip压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_proxied expired no-cache no-store private must-revalidate auth;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/javascript application/json;
    
    # API代理配置
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
        
        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    # 健康检查端点
    location /health {
        proxy_pass http://127.0.0.1:5000/health;
        access_log off;
    }
    
    # 限制请求大小
    client_max_body_size 10M;
}
```

```bash
# 启用站点配置
sudo ln -s /etc/nginx/sites-available/lvtong-api /etc/nginx/sites-enabled/

# 禁用默认站点（如果存在）
sudo rm -f /etc/nginx/sites-enabled/default

# 测试Nginx配置
sudo nginx -t

# 重新加载Nginx
sudo nginx -s reload
```

### 4. 配置防火墙和安全组

**阿里云安全组配置：**
1. 登录阿里云控制台 → ECS管理控制台
2. 找到您的ECS实例 → 安全组配置
3. 添加入方向规则：
   - 端口80/tcp，授权对象：0.0.0.0/0
   - 端口443/tcp，授权对象：0.0.0.0/0

**服务器防火墙配置：**
```bash
# 检查防火墙状态
sudo ufw status

# 如果防火墙启用，添加规则
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw reload
```

### 5. 配置HTTPS（推荐）

```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx -y

# 获取SSL证书（替换为您的域名）
sudo certbot --nginx -d your-domain.com

# 设置自动续期
sudo crontab -e
# 添加以下行：
0 12 * * * /usr/bin/certbot renew --quiet
```

## API接口文档

### 基础接口

| 方法 | 路径 | 描述 | 示例响应 |
|------|------|------|----------|
| GET | `/` | 服务状态 | `{"message": "Flask API Server is running!", "status": "success"}` |
| GET | `/health` | 健康检查 | `{"status": "healthy", "message": "API server is running normally"}` |

### 用户管理接口

| 方法 | 路径 | 描述 | 请求体 |
|------|------|------|--------|
| GET | `/api/users` | 获取用户列表 | 无 |
| POST | `/api/users` | 创建用户 | `{"name": "用户名", "email": "邮箱"}` |
| GET | `/api/users/{id}` | 获取单个用户 | 无，需要用户ID |

### 调用示例

```bash
# 获取用户列表
curl -X GET http://your-domain.com/api/users

# 创建用户
curl -X POST http://your-domain.com/api/users \
    -H "Content-Type: application/json" \
    -d '{"name": "张三", "email": "zhangsan@example.com"}'

# 获取单个用户
curl -X GET http://your-domain.com/api/users/1

# 健康检查
curl http://your-domain.com/health
```

## 服务管理

### 启动和停止服务

```bash
# 启动后端服务
docker-compose up -d backend

# 停止后端服务
docker-compose down

# 重启后端服务
docker-compose restart backend

# 查看服务状态
docker-compose ps

# 重启Nginx
sudo nginx -s reload
```

### 日志查看

```bash
# 查看后端应用日志
docker-compose logs -f backend

# 查看最近100行日志
docker-compose logs --tail=100 backend

# 查看Nginx访问日志
sudo tail -f /var/log/nginx/access.log

# 查看Nginx错误日志
sudo tail -f /var/log/nginx/error.log
```

### 服务监控

```bash
# 检查端口占用
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :5000

# 检查Docker容器状态
docker ps
docker stats

# 检查系统资源
htop
df -h
```

## 生产环境优化

### 性能优化

1. **Nginx配置优化**
   - 启用gzip压缩
   - 配置静态文件缓存
   - 调整worker进程数

2. **Docker优化**
   - 使用多阶段构建减小镜像大小
   - 配置合适的资源限制
   - 启用健康检查

3. **应用优化**
   - 使用Gunicorn多worker进程
   - 配置数据库连接池
   - 启用应用缓存

### 安全配置

1. **使用HTTPS** - 生产环境必须配置SSL证书
2. **防火墙配置** - 只开放必要的端口（80, 443）
3. **访问控制** - 配置适当的CORS策略
4. **日志监控** - 配置日志轮转和监控告警
5. **定期更新** - 保持Docker镜像和系统包更新

## 故障排除

### 常见问题

1. **服务无法启动**
   ```bash
   # 检查端口占用
   sudo lsof -i :5000
   sudo lsof -i :80
   
   # 检查Docker状态
   docker-compose ps
   docker-compose logs backend
   ```

2. **API无法访问**
   ```bash
   # 检查防火墙
   sudo ufw status
   
   # 检查服务健康状态
   curl http://localhost:5000/health
   curl http://localhost/health
   
   # 检查Nginx配置
   sudo nginx -t
   ```

3. **性能问题**
   ```bash
   # 查看资源使用
   docker stats
   
   # 调整worker数量（在Dockerfile中修改gunicorn参数）
   # --workers 4     # 根据CPU核心数调整
   ```

## 扩展功能

### 添加数据库支持

可以在`docker-compose.yml`中添加数据库服务（PostgreSQL、MySQL等）：

```yaml
services:
  database:
    image: postgres:15-alpine
    container_name: postgres-db
    restart: unless-stopped
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: myuser
      POSTGRES_PASSWORD: mypassword
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - api-network

volumes:
  postgres_data:
```

### 添加缓存支持

```yaml
services:
  redis:
    image: redis:7-alpine
    container_name: redis-cache
    restart: unless-stopped
    volumes:
      - redis_data:/data
    networks:
      - api-network

volumes:
  redis_data:
```

## 联系信息

如果您在部署过程中遇到问题，请检查：
1. Docker和Docker Compose版本兼容性
2. 服务器防火墙配置
3. 域名DNS解析设置
4. SSL证书配置
