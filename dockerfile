FROM python:3.9-slim

WORKDIR /app

# 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    default-libmysqlclient-dev && \
    rm -rf /var/lib/apt/lists/*

# Python 가상환경 생성
RUN python3 -m venv venv


# requirements.txt 파일 복사
COPY requirements.txt .

RUN /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install --no-cache-dir -r requirements.txt


# 애플리케이션 전체 복사
COPY . .


ENV PATH="/app/venv/bin:$PATH"

EXPOSE 8000


# MongoDB, MySQL 연결 스크립트를 백그라운드에서 실행한 후 FastAPI 앱 실행
CMD ["sh", "-c", "python database/mongodb_connection.py & python database/mysql_connection.py & uvicorn app.main:app --host 0.0.0.0 --port 8000"]

