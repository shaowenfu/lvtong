# LvTong 项目部署指南

本指南将帮助您使用 Docker 在服务器上部署 LvTong 项目。

## 系统要求

- Docker Engine 20.10+
- Docker Compose 2.0+
- 至少 2GB 可用内存
- 至少 10GB 可用磁盘空间

## 快速部署

### 1. 克隆项目

```bash
git clone <your-repository-url>
cd lvtong
```

### 2. 配置环境变量

```bash
# 复制环境变量模板
cp .env.production .env

# 编辑环境变量文件
vim .env
```

**重要配置项：**

```bash
# OpenAI API 配置（必填）
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_API_BASE=https://your-azure-openai-endpoint.openai.azure.com/
OPENAI_API_VERSION=2023-12-01-preview
```

### 3. 启动服务

```bash
# 使用部署脚本（推荐）
./deploy.sh start

# 或者直接使用 docker-compose
docker-compose up -d
```

### 4. 验证部署

```bash
# 检查服务状态
./deploy.sh status

# 查看日志
./deploy.sh logs
```

## 服务架构

项目包含以下服务：

- **MongoDB**: 数据库服务（端口 27017）
- **Backend**: Flask API 服务（端口 5000）
- **Nginx**: 反向代理服务（端口 80/443）

## 部署脚本使用

```bash
# 启动所有服务
./deploy.sh start

# 停止所有服务
./deploy.sh stop

# 重启所有服务
./deploy.sh restart

# 查看实时日志
./deploy.sh logs

# 检查服务状态
./deploy.sh status
```

## 数据持久化

项目使用 Docker 数据卷来持久化数据：

- `mongodb_data`: MongoDB 数据文件
- `mongodb_config`: MongoDB 配置文件
- `backend_logs`: 后端应用日志
- `nginx_logs`: Nginx 访问日志

## 安全配置

### MongoDB 安全

- 默认创建管理员用户：`admin`
- 默认密码：`lvtong_admin_2024`（建议修改）
- 数据库仅绑定到本地接口，不对外暴露

### 网络安全

- 所有服务运行在独立的 Docker 网络中
- 仅 Nginx 对外暴露端口
- 后端服务仅通过 Nginx 代理访问

## 监控和维护

### 健康检查

所有服务都配置了健康检查：

```bash
# 检查 Backend 健康状态
curl http://localhost:5000/health

# 检查 MongoDB 连接
docker-compose exec mongodb mongosh --eval "db.adminCommand('ping')"
```

### 日志管理

```bash
# 查看特定服务日志
docker-compose logs backend
docker-compose logs mongodb
docker-compose logs nginx

# 查看实时日志
docker-compose logs -f
```

### 备份数据

```bash
# 备份 MongoDB 数据
docker-compose exec mongodb mongodump --out /data/backup

# 导出备份文件
docker cp mongodb:/data/backup ./mongodb_backup
```

## 故障排除

### 常见问题

1. **服务启动失败**
   ```bash
   # 检查日志
   docker-compose logs
   
   # 检查端口占用
   netstat -tlnp | grep :5000
   ```

2. **MongoDB 连接失败**
   ```bash
   # 检查 MongoDB 状态
   docker-compose exec mongodb mongosh --eval "db.adminCommand('ping')"
   
   # 重启 MongoDB
   docker-compose restart mongodb
   ```

3. **环境变量未生效**
   ```bash
   # 检查环境变量
   docker-compose config
   
   # 重新构建并启动
   docker-compose up --build -d
   ```

### 性能优化

1. **调整 Worker 数量**
   
   编辑 `backend/Dockerfile`，修改 gunicorn 配置：
   ```dockerfile
   CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "8", "--timeout", "120", "app:app"]
   ```

2. **MongoDB 性能调优**
   
   在 `docker-compose.yml` 中添加 MongoDB 配置：
   ```yaml
   mongodb:
     command: mongod --wiredTigerCacheSizeGB 1.5
   ```

## 更新部署

```bash
# 拉取最新代码
git pull

# 重新构建并部署
docker-compose up --build -d

# 或使用部署脚本
./deploy.sh restart
```

## 生产环境建议

1. **使用 HTTPS**
   - 配置 SSL 证书
   - 启用 HTTP/2
   - 设置安全头

2. **监控告警**
   - 集成 Prometheus + Grafana
   - 设置服务监控
   - 配置告警规则

3. **备份策略**
   - 定期备份数据库
   - 备份配置文件
   - 测试恢复流程

4. **安全加固**
   - 定期更新镜像
   - 扫描安全漏洞
   - 限制网络访问

## 支持

如果遇到问题，请：

1. 查看本文档的故障排除部分
2. 检查项目 Issues
3. 提交新的 Issue 并附上详细日志

---

**注意**: 请确保在生产环境中修改默认密码和敏感配置！