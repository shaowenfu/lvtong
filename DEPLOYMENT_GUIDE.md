# 部署指南 - Windows系统

本指南将帮助您在Windows系统上安装Docker并部署Flask API服务器。

## 📋 系统要求

- Windows 10 版本 2004 及更高版本（内部版本 19041 及更高版本）或 Windows 11
- 启用 WSL 2 功能
- 启用虚拟化功能
- 至少 4GB RAM

## 🔧 安装步骤

### 1. 启用 WSL 2

1. **以管理员身份打开 PowerShell**，运行以下命令：
   ```powershell
   # 启用 WSL 功能
   dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
   
   # 启用虚拟机平台功能
   dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
   ```

2. **重启计算机**

3. **下载并安装 WSL2 Linux 内核更新包**：
   - 访问：https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi
   - 下载并安装

4. **设置 WSL 2 为默认版本**：
   ```powershell
   wsl --set-default-version 2
   ```

### 2. 安装 Docker Desktop

1. **下载 Docker Desktop**：
   - 访问：https://www.docker.com/products/docker-desktop/
   - 下载 Windows 版本

2. **安装 Docker Desktop**：
   - 运行下载的安装程序
   - 确保选中 "Use WSL 2 instead of Hyper-V" 选项
   - 完成安装后重启计算机

3. **启动 Docker Desktop**：
   - 从开始菜单启动 Docker Desktop
   - 等待 Docker 引擎启动完成

4. **验证安装**：
   ```powershell
   docker --version
   docker-compose --version
   ```

### 3. 部署 Flask API 服务器

1. **打开 PowerShell 或命令提示符**，导航到项目目录：
   ```powershell
   cd E:\all_workspace\Full_stack_workspace\Lvtong
   ```

2. **构建并启动服务**：
   ```powershell
   # 构建并启动所有服务（后台运行）
   docker-compose up --build -d
   
   # 查看服务状态
   docker-compose ps
   
   # 查看日志
   docker-compose logs -f
   ```

3. **测试 API 服务**：
   ```powershell
   # 测试健康检查接口
   curl http://localhost/health
   
   # 或者在浏览器中访问
   # http://localhost/health
   # http://localhost/api/users
   ```

## 🚀 快速启动命令

创建一个批处理文件 `start_server.bat` 来快速启动服务：

```batch
@echo off
echo 正在启动 Flask API 服务器...
cd /d "E:\all_workspace\Full_stack_workspace\Lvtong"
docker-compose up --build -d
echo.
echo 服务启动完成！
echo 访问地址：http://localhost
echo 健康检查：http://localhost/health
echo API接口：http://localhost/api/users
echo.
echo 查看日志：docker-compose logs -f
echo 停止服务：docker-compose down
pause
```

## 🛠️ 常用管理命令

```powershell
# 查看运行中的容器
docker-compose ps

# 查看日志
docker-compose logs -f
docker-compose logs -f backend
docker-compose logs -f nginx

# 重启服务
docker-compose restart
docker-compose restart backend

# 停止服务
docker-compose stop

# 停止并删除容器
docker-compose down

# 停止并删除容器、网络、镜像
docker-compose down --rmi all

# 查看资源使用情况
docker stats

# 进入容器内部
docker-compose exec backend bash
docker-compose exec nginx sh
```

## 🔍 故障排除

### Docker Desktop 无法启动

1. **检查 WSL 2 是否正确安装**：
   ```powershell
   wsl --list --verbose
   ```

2. **检查虚拟化是否启用**：
   - 打开任务管理器 → 性能 → CPU
   - 确认 "虚拟化" 显示为 "已启用"

3. **重置 Docker Desktop**：
   - Docker Desktop → Settings → Reset → Reset to factory defaults

### 端口冲突

如果 80 端口被占用，可以修改 `docker-compose.yml` 中的端口映射：

```yaml
nginx:
  ports:
    - "8080:80"  # 改为使用 8080 端口
    - "8443:443"
```

然后访问 `http://localhost:8080`

### 防火墙问题

如果无法访问服务，检查 Windows 防火墙设置：

1. 打开 Windows 安全中心
2. 防火墙和网络保护
3. 允许应用通过防火墙
4. 确保 Docker Desktop 被允许

## 📱 Flutter 应用调用示例

在 Flutter 应用中调用 API：

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  // 本地开发环境
  static const String baseUrl = 'http://localhost';
  // 生产环境（替换为你的域名）
  // static const String baseUrl = 'https://api.yourdomain.com';
  
  // 获取用户列表
  static Future<List<dynamic>> getUsers() async {
    final response = await http.get(
      Uri.parse('$baseUrl/api/users'),
      headers: {'Content-Type': 'application/json'},
    );
    
    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      return data['data'];
    } else {
      throw Exception('Failed to load users');
    }
  }
  
  // 创建用户
  static Future<Map<String, dynamic>> createUser(String name, String email) async {
    final response = await http.post(
      Uri.parse('$baseUrl/api/users'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({'name': name, 'email': email}),
    );
    
    if (response.statusCode == 201) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to create user');
    }
  }
}
```

## 🌐 生产环境部署

### 阿里云 ECS 部署

1. **购买阿里云 ECS 实例**
2. **配置安全组**：开放 80 和 443 端口
3. **安装 Docker**：
   ```bash
   # 更新系统
   sudo apt update && sudo apt upgrade -y
   
   # 安装 Docker
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   
   # 安装 Docker Compose
   sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

4. **上传项目文件**：
   ```bash
   scp -r ./Lvtong root@your-server-ip:/opt/
   ```

5. **启动服务**：
   ```bash
   cd /opt/Lvtong
   docker-compose up -d --build
   ```

### 域名和 SSL 配置

1. **配置域名解析**：将域名 A 记录指向服务器 IP
2. **申请 SSL 证书**（推荐使用 Let's Encrypt）
3. **修改 nginx.conf**：启用 HTTPS 配置
4. **重启服务**：`docker-compose restart nginx`

## 📞 技术支持

如果遇到问题，请检查：

1. **Docker 版本**：确保使用最新版本
2. **系统要求**：确认系统满足最低要求
3. **网络连接**：确保网络正常
4. **端口占用**：检查端口是否被其他程序占用
5. **日志信息**：查看详细的错误日志

---

**注意**：首次启动可能需要下载 Docker 镜像，请耐心等待。建议在良好的网络环境下进行部署。