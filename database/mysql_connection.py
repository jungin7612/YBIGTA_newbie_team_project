from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 환경 변수에서 AWS RDS MySQL 정보 가져오기
user = os.getenv('MYSQL_USER')
passwd = os.getenv('MYSQL_PASSWORD')
host = os.getenv('MYSQL_HOST')  # AWS RDS 엔드포인트
port = os.getenv('MYSQL_PORT')
db = os.getenv('MYSQL_DATABASE')

# SQLAlchemy MySQL 연결 URL
DB_URL = f'mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}?charset=utf8mb4'

# 데이터베이스 엔진 생성
engine = create_engine(DB_URL, echo=True)

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 연결 테스트 함수


def test_connection():
    try:
        session = SessionLocal()
        print("✅ Successfully connected to AWS RDS MySQL!")
        session.close()
    except Exception as e:
        print("❌ Connection failed:", e)


# 실행
if __name__ == "__main__":
    test_connection()
