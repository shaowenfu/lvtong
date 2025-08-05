# Dozzle 日志查看器配置指南

## 概述

Dozzle 是一个轻量级的 Docker 日志查看器，提供了简洁易用的 Web 界面来实时查看容器日志。本项目已集成 Dozzle 服务，可以方便地监控所有容器的日志输出。

## 功能特性

- 🔍 实时日志查看
- 📊 多容器日志聚合
- 🎨 现代化 Web 界面
- 🔒 安全的本地访问
- 📱 响应式设计，支持移动端
- 🚀 零配置，开箱即用

## 配置说明

### Docker Compose 配置

已在 `docker-compose.yml` 中添加了 Dozzle 服务：

```yaml
# Dozzle日志查看器
dozzle:
  image: amir20/dozzle:latest
  container_name: dozzle
  restart: unless-stopped
  ports:
    - "127.0.0.1:8080:8080"  # 只绑定到本地，通过nginx代理
  volumes:
    - /var/run/docker.sock:/var/run/docker.sock:ro
  environment:
    - DOZZLE_NO_ANALYTICS=true
    - DOZZLE_LEVEL=info
    - DOZZLE_TAILSIZE=300
    - DOZZLE_FILTER="name=mongodb,flask-api,nginx-proxy,mongo-express"
  networks:
    - api-network
  healthcheck:
    test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost:8080"]
    interval: 30s
    timeout: 10s
    retries: 3
    start_period: 10s
```

### Nginx 反向代理配置

已在 `nginx/nginx.conf` 中为所有 server 块添加了 `/logs` 路径的代理配置：

```nginx
# Dozzle logs viewer
location /logs {
    proxy_pass http://dozzle:8080;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

## 部署步骤

### 1. 停止现有服务（如果正在运行）

```bash
cd /home/sherwen/projects/lvtong
docker-compose down
```

### 2. 重新构建并启动服务

```bash
# 重新构建并启动所有服务
docker-compose up -d --build

# 或者只启动新的 dozzle 服务
docker-compose up -d dozzle
```

### 3. 验证服务状态

```bash
# 检查所有容器状态
docker-compose ps

# 检查 dozzle 容器日志
docker-compose logs dozzle

# 检查 nginx 配置是否正确
docker-compose exec nginx nginx -t
```

### 4. 重新加载 Nginx 配置

```bash
# 重新加载 nginx 配置
docker-compose exec nginx nginx -s reload
```

## 访问方式

### 通过域名访问（推荐）

- **HTTPS**: https://lvtong.sherwenfu.com/logs
- **HTTP**: http://lvtong.sherwenfu.com/logs（会自动重定向到 HTTPS）

### 通过 IP 访问

- **HTTP**: http://47.108.89.109/logs

### 直接访问（仅本地）

- **本地**: http://localhost:8080（仅在服务器本地可访问）

## 使用说明

### 界面功能

1. **容器列表**: 左侧显示所有可监控的容器
2. **日志查看**: 点击容器名称查看实时日志
3. **搜索过滤**: 支持关键词搜索和日志级别过滤
4. **自动刷新**: 实时显示最新日志
5. **下载日志**: 支持下载日志文件

### 监控的容器

当前配置监控以下容器的日志：
- `mongodb` - MongoDB 数据库
- `flask-api` - Flask 后端服务
- `nginx-proxy` - Nginx 反向代理
- `mongo-express` - MongoDB 管理界面
- `dozzle` - Dozzle 自身（如需要）

### 日志级别

- **ERROR**: 错误信息
- **WARN**: 警告信息
- **INFO**: 一般信息
- **DEBUG**: 调试信息

## 安全考虑

1. **本地绑定**: Dozzle 服务只绑定到 `127.0.0.1:8080`，不直接暴露到外网
2. **代理访问**: 通过 Nginx 反向代理访问，可以利用现有的 SSL 证书和安全配置
3. **只读权限**: Docker socket 以只读模式挂载，Dozzle 无法控制容器
4. **无分析**: 已禁用 Dozzle 的分析功能（`DOZZLE_NO_ANALYTICS=true`）

## 故障排除

### 常见问题

1. **无法访问 /logs 路径**
   ```bash
   # 检查 nginx 配置
   docker-compose exec nginx nginx -t
   # 重新加载配置
   docker-compose exec nginx nginx -s reload
   ```

2. **Dozzle 容器无法启动**
   ```bash
   # 检查容器日志
   docker-compose logs dozzle
   # 检查 Docker socket 权限
   ls -la /var/run/docker.sock
   ```

3. **看不到某些容器的日志**
   - 检查 `DOZZLE_FILTER` 环境变量配置
   - 确认容器名称是否正确

### 日志查看命令

```bash
# 查看 dozzle 服务日志
docker-compose logs -f dozzle

# 查看 nginx 访问日志
docker-compose logs -f nginx

# 查看所有服务状态
docker-compose ps
```

## 自定义配置

### 修改监控的容器

编辑 `docker-compose.yml` 中的 `DOZZLE_FILTER` 环境变量：

```yaml
environment:
  - DOZZLE_FILTER="name=mongodb,flask-api,nginx-proxy,mongo-express,your-new-container"
```

### 修改日志显示行数

```yaml
environment:
  - DOZZLE_TAILSIZE=500  # 默认显示 500 行
```

### 修改访问路径

如需修改访问路径（如改为 `/admin/logs`），需要同时修改：
1. `nginx/nginx.conf` 中的 `location` 路径
2. 重新加载 Nginx 配置

## 维护建议

1. **定期更新**: 定期更新 Dozzle 镜像到最新版本
2. **日志轮转**: 配置 Docker 日志轮转，避免日志文件过大
3. **监控资源**: 监控 Dozzle 容器的资源使用情况
4. **备份配置**: 定期备份 Docker Compose 和 Nginx 配置文件

---

**注意**: 本配置适用于生产环境，已考虑安全性和性能优化。如有特殊需求，请根据实际情况调整配置。