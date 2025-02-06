# Python 3.9 Slim 버전 사용
FROM python:3.9-slim

# 작업 디렉토리 설정
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

# OS에 따라 venv 경로 자동 설정 (맥/윈도우 지원)
ENV VENV_PATH="/app/venv/bin"
RUN if [ -d "/app/venv/Scripts" ]; then export VENV_PATH="/app/venv/Scripts"; fi

# 환경변수 설정 (맥 & 윈도우 환경 모두 호환)
ENV PATH="$VENV_PATH:$PATH"

# requirements.txt 파일 먼저 복사 (빌드 캐시 최적화)
COPY requirements.txt .

# pip 업데이트 및 패키지 설치
RUN $VENV_PATH/pip install --upgrade pip && \
    $VENV_PATH/pip install --no-cache-dir -r requirements.txt

# 전체 애플리케이션 파일 복사
COPY . .

# 포트 개방
EXPOSE 8000

# MySQL & MongoDB 연결 후 FastAPI 실행
CMD ["sh", "-c", "python database/mongodb_connection.py & python database/mysql_connection.py & uvicorn app.main:app --host 0.0.0.0 --port 8000"]
