# ── Build stage ──────────────────────────────────────────────────────────────
FROM python:3.12-alpine AS builder

WORKDIR /app

# 安装编译依赖（sqlite3 已内置于 alpine，无需额外安装）
RUN apk add --no-cache gcc musl-dev

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Runtime stage ─────────────────────────────────────────────────────────────
FROM python:3.12-alpine

WORKDIR /app

# 从 builder 拷贝已安装的依赖
COPY --from=builder /install /usr/local

# 拷贝应用代码
COPY app.py .
COPY templates/ templates/

# 数据目录（挂载 volume 持久化 SQLite）
RUN mkdir -p /app/data

EXPOSE 5000

ENV FLASK_ENV=production \
    PYTHONUNBUFFERED=1

CMD ["python", "app.py"]
