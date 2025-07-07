# 使用Python 3.11官方镜像作为基础镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_ENV=production

# 更换为中科大apt源，加速依赖安装
RUN echo "deb https://mirrors.ustc.edu.cn/debian/ bookworm main contrib non-free\n\
deb https://mirrors.ustc.edu.cn/debian/ bookworm-updates main contrib non-free\n\
deb https://mirrors.ustc.edu.cn/debian/ bookworm-backports main contrib non-free\n\
deb https://mirrors.ustc.edu.cn/debian-security/ bookworm-security main contrib non-free" > /etc/apt/sources.list

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 复制requirements.txt并安装Python依赖
COPY requirements.txt .
# 配置pip使用国内镜像源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/ && \
    pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn && \
    pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY . .

# 创建非root用户
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
# USER appuser

# 暴露端口
EXPOSE 5000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# 使用gunicorn启动应用（生产环境推荐）
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "--log-level", "debug", "app:app"]
