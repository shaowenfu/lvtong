@echo off
chcp 65001 >nul
echo ========================================
echo     Flask API 服务器停止脚本
echo ========================================
echo.

:: 切换到项目目录
cd /d "%~dp0"
echo 当前目录：%CD%
echo.

:: 显示当前运行的服务
echo [1/3] 当前运行的服务：
docker-compose ps
echo.

:: 询问用户选择停止方式
echo [2/3] 请选择停止方式：
echo 1. 停止服务（保留容器和数据）
echo 2. 停止并删除容器（保留镜像和数据卷）
echo 3. 完全清理（删除容器、网络、镜像）
echo 4. 取消操作
echo.
set /p choice=请输入选择 (1-4): 

if "%choice%"=="1" (
    echo.
    echo 正在停止服务...
    docker-compose stop
    if %errorlevel% equ 0 (
        echo ✅ 服务已停止
        echo 💡 使用 docker-compose start 可以重新启动
    ) else (
        echo ❌ 停止服务失败
    )
) else if "%choice%"=="2" (
    echo.
    echo 正在停止并删除容器...
    docker-compose down
    if %errorlevel% equ 0 (
        echo ✅ 容器已删除
        echo 💡 数据卷和镜像已保留，下次启动会更快
    ) else (
        echo ❌ 删除容器失败
    )
) else if "%choice%"=="3" (
    echo.
    echo ⚠️  警告：这将删除所有相关的容器、网络和镜像！
    set /p confirm=确认执行完全清理？(y/N): 
    if /i "%confirm%"=="y" (
        echo 正在执行完全清理...
        docker-compose down --rmi all --volumes --remove-orphans
        if %errorlevel% equ 0 (
            echo ✅ 完全清理完成
            echo 💡 下次启动需要重新下载和构建镜像
        ) else (
            echo ❌ 清理失败
        )
    ) else (
        echo 操作已取消
    )
) else if "%choice%"=="4" (
    echo 操作已取消
) else (
    echo ❌ 无效选择
)

echo.
echo [3/3] 当前状态：
docker-compose ps

echo.
echo ========================================
echo 操作完成
echo ========================================
echo.
echo 按任意键退出...
pause >nul