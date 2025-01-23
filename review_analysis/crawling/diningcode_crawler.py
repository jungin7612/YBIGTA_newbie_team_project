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

class DiningCodeCrawler(BaseCrawler):
    def __init__(self, output_dir: str):
        super().__init__(output_dir)
        self.base_url = 'https://www.diningcode.com/profile.php?rid=ZKUECqHgsTki'
        self.reviews_data = []

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
        """다이닝코드 리뷰 데이터 크롤링"""
        print("리뷰 데이터를 크롤링합니다...")

        while True:
            try:
                more_button = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div#div_more_review button.More__Review__Button'))
                )
                self.driver.execute_script("arguments[0].click();", more_button)
                time.sleep(3)
            except:
                print("모든 리뷰가 로드되었습니다.")
                break

        soup = BeautifulSoup(self.driver.page_source, 'html.parser')

        # 별점 가져오기 (숫자만 추출)
        ratings = [rating.text.strip().replace("점", "") for rating in soup.select('p.point-detail span.total_score')]

        # 리뷰 텍스트 가져오기 (빈 리뷰 처리)
        reviews = [review.get_text(separator=" ", strip=True) if review.get_text(strip=True) else "리뷰 없음" 
                   for review in soup.select('p.review_contents.btxt')]

        # 날짜 가져오기
        dates = [date.text.strip() for date in soup.select('div.date')]

        print(f"수집된 개수 - 별점: {len(ratings)}, 리뷰: {len(reviews)}, 날짜: {len(dates)}")

        seen_reviews = set()
        for rating, review, date in zip(ratings, reviews, dates):
            unique_key = f"{rating}_{review}_{date}"
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

        df = pd.DataFrame(self.reviews_data)

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"디렉토리를 생성했습니다: {self.output_dir}")

        output_file = os.path.join(self.output_dir, "reviews_diningcode.csv")
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"데이터가 {output_file}에 저장되었습니다.")

