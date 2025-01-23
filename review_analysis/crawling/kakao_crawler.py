import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException
import time
from typing import List, TypedDict


class Review(TypedDict):
    text: str
    date: str
    rating: float


class ExampleCrawler:
    def __init__(self, output_dir: str):
        self.base_url = 'https://place.map.kakao.com/1011256721'
        self.driver = None
        self.output_dir = output_dir
        self.reviews: List[Review] = []

    def start_browser(self):
        try:
            options = webdriver.ChromeOptions()
            # options.add_argument('--headless')  # GUI 없이 실행
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('window-size=1920x1080')

            self.driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), options=options
            )
            print("Browser started successfully.")
        except Exception as e:
            print(f"Error starting browser: {e}")
            self.driver = None

    def scrape_reviews(self):
        self.reviews = []  # 크롤링 전에 초기화
        try:
            if not self.driver:
                raise Exception(
                    "Browser not started. Call start_browser() first.")

            self.driver.get(f"{self.base_url}#comment")
            print(f"Accessing {self.base_url}#comment")

            click_count = 0
            max_clicks = 75
            while click_count < max_clicks:
                try:
                    # "더보기" 버튼을 div.evaluation_review 내에서 찾기
                    load_more_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable(
                            (By.CSS_SELECTOR, "div.evaluation_review a.link_more")
                        )
                    )

                    # 버튼이 보이도록 스크롤 (옵션: 약간의 오프셋 추가)
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center', inline: 'center'});", load_more_button
                    )

                    # JavaScript를 사용하여 클릭
                    self.driver.execute_script(
                        "arguments[0].click();", load_more_button)
                    click_count += 1
                    print(f"'더보기' 버튼 클릭: {click_count}/{max_clicks}")

                    # 새 리뷰가 로드될 시간을 기다림 (짧은 대기 시간으로 최적화)
                    time.sleep(0.5)  # 짧은 대기 시간 추가

                except TimeoutException:
                    print("더 이상 '더보기' 버튼이 없거나 로딩 시간이 초과되었습니다.")
                    break
                except Exception as e:
                    print(f"Unexpected error while clicking '더보기': {e}")
                    break

            # 모든 "더보기" 버튼 클릭이 완료된 후 모든 리뷰를 한 번에 수집
            all_review_elements = self.driver.find_elements(
                By.CSS_SELECTOR, "ul.list_evaluation li")
            print(f"총 리뷰 개수: {len(all_review_elements)}")

            for idx, element in enumerate(all_review_elements, start=1):
                try:
                    # 리뷰 텍스트
                    review_text_element = element.find_element(
                        By.CSS_SELECTOR, "p.txt_comment > span")
                    review_text = review_text_element.text.strip(
                    ) if review_text_element.text else "내용 없음"

                    # 작성 날짜
                    review_date = element.find_element(
                        By.CSS_SELECTOR, "div.unit_info span.time_write").text.strip()

                    # 평점 (스타 비율로부터 추출)
                    star_width = element.find_element(
                        By.CSS_SELECTOR, "div.star_info span.inner_star").get_attribute("style")
                    star_rating = float(star_width.split(
                        "width:")[1].strip('% ;')) / 20.0
                    star_rating = round(star_rating, 1)

                    self.reviews.append({
                        "text": review_text,
                        "date": review_date,
                        "rating": star_rating,
                    })
                    print(f"리뷰 추가: {idx}번째 리뷰")

                except Exception as e:
                    print(f"리뷰 데이터를 추출하는 중 오류 발생: {e}")

        except Exception as e:
            print(f"리뷰 스크래이핑 중 오류 발생: {e}")
        finally:
            print(f"스크랩된 리뷰 수: {len(self.reviews)}")

    def save_to_database(self):
        if not self.reviews:
            print("No reviews to save.")
            return

        output_file = f"{self.output_dir}/reviews_kakaomap.csv"
        try:
            # CSV 파일로 저장
            with open(output_file, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(
                    f, fieldnames=["text", "date", "rating"])
                writer.writeheader()  # 헤더 작성
                writer.writerows(self.reviews)  # 데이터 작성

            print(f"Reviews saved to {output_file}.")
        except Exception as e:
            print(f"Error while saving reviews: {e}")
