from pymongo import MongoClient
from dotenv import load_dotenv
import os
import pandas as pd

# .env 파일 로드
load_dotenv()

# MongoDB 연결
mongo_url = os.getenv("MONGO_URL")
mongo_client = MongoClient(mongo_url)
mongo_db = mongo_client.get_database("Cluster0")  # 데이터베이스 자동 선택

print(f"✅ MongoDB Atlas 연결 완료! (DB: {mongo_db.name})")

# # 현재 파일(`connection.py`)이 있는 디렉토리 기준으로 파일 경로 설정
# base_dir = os.path.dirname(os.path.abspath(__file__))

# # 컬렉션 이름 매핑 (파일별)
# collection_mapping = {
#     os.path.join(base_dir, "reviews_kakaomap.csv"): os.getenv("COLLECTION_1"),
#     os.path.join(base_dir, "reviews_naver.csv"): os.getenv("COLLECTION_2"),
#     os.path.join(base_dir, "reviews_googlemaps.csv"): os.getenv("COLLECTION_3"),
# }

# # CSV 파일을 각각의 컬렉션에 업로드
# for file_path, collection_name in collection_mapping.items():
#     collection = mongo_db[collection_name]

#     # CSV 파일 존재 여부 확인
#     if not os.path.exists(file_path):
#         print(f"⚠️ 파일 없음: {file_path} → 스킵")
#         continue

#     # CSV 파일 읽기
#     df = pd.read_csv(file_path)

#     # DataFrame을 딕셔너리 리스트로 변환 후 MongoDB에 삽입
#     data = df.to_dict(orient="records")
#     collection.insert_many(data)

#     print(f"✅ {file_path} → {collection_name} 컬렉션에 데이터 업로드 완료!")
