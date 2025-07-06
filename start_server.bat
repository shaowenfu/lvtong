@echo off
chcp 65001 >nul
echo ========================================
echo     Flask API 服务器启动脚本
echo ========================================
echo.

:: 检查Docker是否安装
echo [1/4] 检查 Docker 安装状态...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker 未安装或未启动！
    echo.
    echo 请先安装 Docker Desktop：
    echo https://www.docker.com/products/docker-desktop/
    echo.
    echo 详细安装指南请查看：DEPLOYMENT_GUIDE.md
    pause
    exit /b 1
)
echo ✅ Docker 已安装

:: 检查Docker Compose是否可用
echo [2/4] 检查 Docker Compose...
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker Compose 不可用！
    echo 请确保 Docker Desktop 正在运行
    pause
    exit /b 1
)
echo ✅ Docker Compose 可用

:: 切换到项目目录
echo [3/4] 切换到项目目录...
cd /d "%~dp0"
echo ✅ 当前目录：%CD%

:: 启动服务
echo [4/4] 启动 Flask API 服务器...
echo.
echo 正在构建和启动容器，首次运行可能需要几分钟...
docker-compose up --build -d

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo 🎉 服务启动成功！
    echo ========================================
    echo.
    echo 📍 访问地址：
    echo    主页：      http://localhost
    echo    健康检查：  http://localhost/health
    echo    用户API：   http://localhost/api/users
    echo.
    echo 📋 管理命令：
    echo    查看状态：  docker-compose ps
    echo    查看日志：  docker-compose logs -f
    echo    停止服务：  docker-compose stop
    echo    完全清理：  docker-compose down
    echo.
    echo 📖 更多信息请查看 README.md
    echo ========================================
) else (
    echo.
    echo ❌ 服务启动失败！
    echo.
    echo 请检查错误信息并参考 DEPLOYMENT_GUIDE.md
    echo 或运行以下命令查看详细日志：
    echo docker-compose logs
)

echo.
echo 按任意键退出...
pause >nul