from fastapi import APIRouter, HTTPException, Depends, status
from app.dependencies import get_mongo_client
from app.responses.base_response import BaseResponse
from pymongo.collection import Collection
from review_analysis.preprocessing.kakao_processor import KakaoProcessor
from review_analysis.preprocessing.googlemaps_processor import GoogleMapsProcessor
from review_analysis.preprocessing.naver_processor import NaverProcessor

review = APIRouter(prefix="/api/review")

def get_review_collection():
    client = get_mongo_client()
    return client.get_database("review_db").get_collection("reviews")

def get_preprocessor(site_name: str):
    if site_name.lower() == "kakao":
        return KakaoProcessor()
    elif site_name.lower() == "google":
        return GoogleMapsProcessor()
    elif site_name.lower() == "naver":
        return NaverProcessor()
    else:
        raise ValueError(f"Unsupported site: {site_name}")

@review.post("/preprocess/{site_name}", status_code=status.HTTP_200_OK)
def preprocess_review(site_name: str, collection: Collection = Depends(get_review_collection)):
    try:
        # MongoDB에서 크롤링 데이터 조회
        reviews = list(collection.find({"site_name": site_name}))
        if not reviews:
            raise ValueError(f"No reviews found for site: {site_name}")
        
        # 사이트별 전처리 수행
        preprocessor = get_preprocessor(site_name)
        processed_reviews = [preprocessor.process(review) for review in reviews]
        
        # 전처리된 데이터 저장
        for review in processed_reviews:
            collection.update_one({"_id": review["_id"]}, {"$set": review})
        
        return BaseResponse(status="success", data=processed_reviews, message=f"Review preprocessing successful for {site_name}.")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
