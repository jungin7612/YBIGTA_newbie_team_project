from sqlalchemy import Column, Integer, String, text
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


# ✅ 3. 생성된 데이터베이스에 다시 연결
DB_URL = f"mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}?charset=utf8mb4"
engine = create_engine(DB_URL, echo=True)

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ✅ 6. 연결 테스트 함수


def test_connection():
    try:
        session = SessionLocal()
        print("✅ Successfully connected to AWS RDS MySQL!")
        session.close()
    except Exception as e:
        print("❌ Connection failed:", e)


# ✅ 7. 테이블 목록 확인
def check_tables():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SHOW TABLES;"))
            tables = [row[0] for row in result]
            print("📌 Existing Tables:", tables)

            if "users" in tables:
                print("✅ 'users' table exists!")
                # 'users' 테이블 구조 확인
                describe_result = conn.execute(text("DESCRIBE users;"))
                for row in describe_result:
                    print(row)
            else:
                print("❌ 'users' table does not exist.")
    except Exception as e:
        print("❌ Error checking tables:", e)


# ✅ 8. 실행
if __name__ == "__main__":
    test_connection()  # MySQL 연결 확인
    check_tables()  # 테이블 확인
