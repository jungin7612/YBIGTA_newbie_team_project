from review_analysis.crawling.base_crawler import BaseCrawler
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import time
import os

from typing import List, Dict

class GoogleMapsCrawler(BaseCrawler):
    def __init__(self, output_dir: str):
        super().__init__(output_dir)
        self.base_url = 'https://www.google.com/maps/place/%ED%8C%8C%EC%9D%B4%ED%99%80/data=!4m18!1m9!3m8!1s0x357c98949e1b2c2f:0x3d05b9bcbf909f3!2z7YyM7J207ZmA!8m2!3d37.5570004!4d126.9350473!9m1!1b1!16s%2Fg%2F1hc4q16_8!3m7!1s0x357c98949e1b2c2f:0x3d05b9bcbf909f3!8m2!3d37.5570004!4d126.9350473!9m1!1b1!16s%2Fg%2F1hc4q16_8?hl=ko&entry=ttu&g_ep=EgoyMDI1MDExNS4wIKXMDSoASAFQAw%3D%3D'
        self.reviews_data: List[Dict[str, str]] = []

    def start_browser(self):
        """브라우저 시작 및 URL 접속"""
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.base_url)
        time.sleep(5)

    def scrape_reviews(self):
        """구글맵 리뷰 데이터 크롤링"""
        print("리뷰 데이터를 크롤링합니다...")

        try:
            scrollable_div = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.m6QErb.DxyBCb.kA9KIf.dS8AEf'))
            )
        except EC.TimeoutException:
            print("리뷰 섹션을 찾을 수 없습니다. URL을 확인하세요.")
            return

        last_review_count = 0
        max_attempts = 200
        attempts = 0

        while attempts < max_attempts:
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scrollable_div)
            time.sleep(3)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            current_review_count = len(soup.select('span.kvMYJc[role="img"]'))
            print(f"스크롤 {attempts + 1}/{max_attempts}, 리뷰 개수: {current_review_count}")

            if current_review_count == last_review_count and attempts > 20:
                print("모든 리뷰가 로드되었습니다.")
                break
            last_review_count = current_review_count
            attempts += 1

        # '더보기' 버튼 처리
        while True:
            more_buttons = self.driver.find_elements(By.CSS_SELECTOR, 'button.w8nwRe.kyuRq')
            if not more_buttons:
                break
            for btn in more_buttons:
                try:
                    self.driver.execute_script("arguments[0].click();", btn)
                    time.sleep(2)
                except Exception as e:
                    print(f"'더보기' 버튼 클릭 중 오류 발생: {e}")

        # 화면 조정 및 추가 스크롤링
        for _ in range(5):
            self.driver.execute_script("arguments[0].scrollTop -= 500", scrollable_div)
            time.sleep(1)
            self.driver.execute_script("arguments[0].scrollTop += 500", scrollable_div)
            time.sleep(3)

        # 페이지 소스를 가져와서 파싱
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        # 별점 가져오기
        ratings = [rating['aria-label'] for rating in soup.select('span.kvMYJc[role="img"]')]

        # 리뷰 텍스트 가져오기 (빈 리뷰 처리)
        review_elements = soup.select('span.wiI7pd')
        reviews = [review.text.strip() if review.text.strip() else "리뷰 없음" for review in review_elements]

        while len(reviews) < len(ratings):
            reviews.append("리뷰 없음")

        # 날짜 가져오기
        dates = [date.text.strip() for date in soup.select('span.rsqaWe')]

        print(f"수집된 개수 - 별점: {len(ratings)}, 리뷰: {len(reviews)}, 날짜: {len(dates)}")

        # 중복 방지 및 데이터 저장
        seen_reviews = set()
        for idx, (rating, review, date) in enumerate(zip(ratings, reviews, dates)):
            unique_key = f"{rating}_{review}_{date}_{idx}"
            if unique_key not in seen_reviews:
                self.reviews_data.append({
                    '별점': rating,
                    '리뷰 내용': review,
                    '날짜': date
                })
                seen_reviews.add(unique_key)

        print(f"총 {len(self.reviews_data)}개의 리뷰를 수집했습니다.")

    def save_to_database(self):
        """수집한 데이터를 CSV 파일로 저장"""
        if not self.reviews_data:
            print("저장할 데이터가 없습니다.")
            return

        # pandas 데이터프레임 생성
        df = pd.DataFrame(self.reviews_data)

        # 디렉토리 생성 확인
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"디렉토리를 생성했습니다: {self.output_dir}")

        # CSV 파일로 저장
        output_file = os.path.join(self.output_dir, "reviews_googlemaps.csv")
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"데이터가 {output_file}에 저장되었습니다.")










