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

from datetime import datetime

class NaverCrawler(BaseCrawler):
    def __init__(self, output_dir: str):
        super().__init__(output_dir)
        self.base_url = 'https://map.naver.com/p/entry/place/21306384?c=15.00,0,0,0,dh&placePath=/review'
        self.reviews = []
        self.driver = None
        self.cutoff_date = datetime(2021, 10, 1)  # 2021년 10월 1일 이전 날짜만 저장

    def start_browser(self):
        chrome_options = Options()
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.base_url)
        self.driver.implicitly_wait(20)
        print('"파이홀" 네이버 리뷰 페이지 로딩 성공')

    # def scrape_reviews(self):
    #     columns = ['content', 'date', 'stars']
    #     values = []
    #     n = 0
    #     seen_reviews = set()
    #     previous_review_count = 0  # 이전에 크롤링된 리뷰 수

    #     try:
    #         iframe = self.driver.find_element(By.ID, 'entryIframe')
    #         self.driver.switch_to.frame(iframe)
    #         print("iframe 전환 성공")

    #         while True:
    #             try:
    #                 # 리뷰 데이터 대기
    #                 WebDriverWait(self.driver, 10).until(
    #                     EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.pui__X35jYm.place_apply_pui.EjjAW'))
    #                 )
    #                 reviews = self.driver.find_elements(By.CSS_SELECTOR, 'li.pui__X35jYm.place_apply_pui.EjjAW')

    #                 # 새로운 리뷰만 처리
    #                 if len(reviews) <= previous_review_count:
    #                     print(f"새로운 리뷰 없음. 현재 리뷰 수: {len(reviews)}, 이전 리뷰 수: {previous_review_count}")
    #                     break

    #                 for i in range(previous_review_count, len(reviews)):
    #                     review = reviews[i]
    #                     blank = []
    #                     try:
    #                         # 리뷰 내용 가져오기
    #                         content_tag = review.find_element(By.CSS_SELECTOR, 'a[data-pui-click-code="rvshowmore"]')
    #                         content = content_tag.text.strip() if content_tag else None
    #                         content_key = content.lower().replace(" ", "") if content else None

    #                         if content_key in seen_reviews:
    #                             continue

    #                         seen_reviews.add(content_key)
    #                         n += 1
    #                         blank.append(content or "내용 없음")
    #                     except Exception:
    #                         blank.append("Error")

    #                     try:
    #                         # 날짜 및 형제 태그 데이터 가져오기
    #                         time_tag = review.find_element(By.TAG_NAME, 'time')
    #                         if time_tag:
    #                             date_str = time_tag.text.strip()
    #                             print(f"날짜 데이터: {date_str}")  # 디버깅용 로그 추가

    #                             if date_str != "날짜 없음":
    #                                 try:
    #                                     if '.' in date_str:
    #                                         # 형식 판별 및 처리
    #                                         parts = date_str.split('.')
    #                                         if len(parts) == 3:  # 형식: 1.17.금
    #                                             month, day, _ = parts
    #                                             year = datetime.now().year  # 연도가 없는 경우 현재 연도 사용
    #                                             clean_date = f"{year}-{int(month):02d}-{int(day):02d}"
    #                                             review_date = datetime.strptime(clean_date, '%Y-%m-%d')
    #                                             blank.append(review_date.strftime('%Y-%m-%d'))
    #                                         elif len(parts) == 4:  # 형식: 24.12.24.화
    #                                             year, month, day, _ = parts
    #                                             year = int(year) + 2000 if int(year) < 100 else int(year)  # 2자리 연도 처리
    #                                             clean_date = f"{year}-{int(month):02d}-{int(day):02d}"
    #                                             review_date = datetime.strptime(clean_date, '%Y-%m-%d')
    #                                             blank.append(review_date.strftime('%Y-%m-%d'))
    #                                         else:
    #                                             raise ValueError("알 수 없는 날짜 형식")
    #                                     else:
    #                                         raise ValueError("알 수 없는 날짜 형식")
    #                                 except ValueError as ve:
    #                                     print(f"날짜 파싱 오류: {ve}, 원본 날짜: {date_str}")
    #                                     blank.append("날짜 형식 오류")
    #                             else:
    #                                 blank.append("날짜 없음")
    #                         else:
    #                             blank.append("날짜 없음")
    #                     except Exception as e:
    #                         print(f"날짜 처리 중 오류 발생: {e}")
    #                         blank.append("Error")

    #                     try:
    #                         # 별점 가져오기
    #                         star_tag = review.find_element(By.CLASS_NAME, 'pui__6abRMf')  # 별점이 포함된 태그 선택
    #                         if star_tag:
    #                             try:
    #                                 svg_tag = star_tag.find_element(By.TAG_NAME, 'svg')  # 별점 SVG 태그 선택
    #                                 star_rating = svg_tag.find_element(By.XPATH, 'following-sibling::text()').strip()  # 별점 값 추출
    #                                 blank.append(star_rating)
    #                             except Exception:
    #                                 print(f"별점 수치 조회 실패: {review.text}")  # 디버깅용 로그
    #                                 blank.append("별점기능 폐지")
    #                         else:
    #                             blank.append("별점기능 폐지")
    #                     except Exception as e:
    #                         blank.append("별점기능 폐지")

    #                     values.append(blank)
    #                     print(f"{n}번째 리뷰 데이터 추가 완료: {blank}")

    #                 previous_review_count = len(reviews)  # 크롤링된 리뷰 수 업데이트

    #                 # "더보기" 버튼 클릭 시도
    #                 try:
    #                     more_button = WebDriverWait(self.driver, 5).until(
    #                         EC.element_to_be_clickable(
    #                             (By.XPATH, '//*[@id="app-root"]/div/div/div/div[6]/div[3]/div[3]/div[2]/div/a')
    #                         )
    #                     )
    #                     more_button.click()
    #                     time.sleep(3)  # 클릭 후 충분히 대기
    #                 except Exception:
    #                     print("더보기 버튼 없음 또는 클릭 실패.")
    #                     break
    #             except Exception as e:
    #                 print(f"리뷰 크롤링 중 오류 발생: {e}")
    #                 break

    #         if values:    
    #             df = pd.DataFrame(values, columns=columns)
    #             self.reviews.append(df)
    #             print("크롤링 완료")
    #         else:
    #             print("크롤링 데이터 없음")
    #         input("브라우저를 닫으려면 Enter를 누르세요...")
    #     except Exception as e:
    #         print(f"iframe 전환 실패 또는 크롤링 오류 발생: {e}")

    def scrape_reviews(self):
        columns = ['content', 'date', 'stars']
        values = []
        n = 0
        seen_reviews = set()
        previous_review_count = 0  # 이전에 크롤링된 리뷰 수

        try:
            iframe = self.driver.find_element(By.ID, 'entryIframe')
            self.driver.switch_to.frame(iframe)
            print("iframe 전환 성공")

            while True:
                try:
                    # 리뷰 데이터 대기 및 전체 HTML 파싱
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.pui__X35jYm.place_apply_pui.EjjAW'))
                    )
                    soup = BeautifulSoup(self.driver.page_source, 'html.parser')
                    reviews = soup.select('li.pui__X35jYm.place_apply_pui.EjjAW')

                    # 새로운 리뷰만 처리
                    if len(reviews) <= previous_review_count:
                        print(f"새로운 리뷰 없음. 현재 리뷰 수: {len(reviews)}, 이전 리뷰 수: {previous_review_count}")
                        break

                    for review in reviews[previous_review_count:]:
                        blank = ["", "", ""]  # 기본값으로 빈 데이터 설정
                        try:
                            # 리뷰 내용 가져오기
                            content_tag = review.select_one('a[data-pui-click-code="rvshowmore"]')
                            content = content_tag.text.strip() if content_tag else ""
                            content_key = content.lower().replace(" ", "") if content else ""

                            if content_key in seen_reviews:
                                continue

                            seen_reviews.add(content_key)
                            n += 1
                            blank[0] = content

                            # 날짜 가져오기
                            time_tag = review.find('time')
                            if time_tag:
                                date_str = time_tag.text.strip()
                                if date_str and '.' in date_str:
                                    parts = date_str.split('.')
                                    if len(parts) == 3:  # 형식: 1.17.금
                                        month, day, _ = parts
                                        year = datetime.now().year
                                        clean_date = f"{year}-{int(month):02d}-{int(day):02d}"
                                        review_date = datetime.strptime(clean_date, '%Y-%m-%d')
                                        blank[1] = review_date.strftime('%Y-%m-%d')
                                    elif len(parts) == 4:  # 형식: 24.12.24.화
                                        year, month, day, _ = parts
                                        year = int(year) + 2000 if int(year) < 100 else int(year)
                                        clean_date = f"{year}-{int(month):02d}-{int(day):02d}"
                                        review_date = datetime.strptime(clean_date, '%Y-%m-%d')
                                        blank[1] = review_date.strftime('%Y-%m-%d')

                            # 별점 가져오기
                            star_tag = review.select_one('.pui__6abRMf')
                            if star_tag:
                                star_rating = star_tag.get_text(strip=True)
                                blank[2] = star_rating

                        except Exception:
                            pass

                        values.append(blank)
                        print(f"{n}번째 리뷰 데이터 추가 완료: {blank}")

                    previous_review_count = len(reviews)  # 크롤링된 리뷰 수 업데이트

                    # "더보기" 버튼 클릭
                    try:
                        more_button = WebDriverWait(self.driver, 5).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, '//*[@id="app-root"]/div/div/div/div[6]/div[3]/div[3]/div[2]/div/a')
                            )
                        )
                        more_button.click()
                        time.sleep(3)  # 클릭 후 충분히 대기
                    except Exception:
                        print("더보기 버튼 없음 또는 클릭 실패.")
                        break
                except Exception as e:
                    print(f"리뷰 크롤링 중 오류 발생: {e}")
                    break

            # 데이터 저장
            if values:
                df = pd.DataFrame(values, columns=columns)
                self.reviews.append(df)
                print("크롤링 완료")
            else:
                print("크롤링 데이터 없음")
            input("브라우저를 닫으려면 Enter를 누르세요...")

        except Exception as e:
            print(f"iframe 전환 실패 또는 크롤링 오류 발생: {e}")



        
        


    def save_to_database(self):
        if not self.reviews:
            print("저장할 리뷰 데이터가 없습니다. 크롤링 데이터를 확인하세요.")
            return
    
        try:
            # 리뷰 데이터를 하나의 DataFrame으로 병합
            final_df = pd.concat(self.reviews, ignore_index=True)
            
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)  # 디렉토리 생성
            output_path = os.path.join(self.output_dir, "reviews_filtered.csv")

            # 지정된 경로에 파일 저장
            final_df.to_csv(output_path, index=False, encoding='utf-8-sig')             
            print(f"리뷰 데이터가 성공적으로 저장되었습니다: {output_path}")
        except Exception as e:
            print(f"데이터 저장 중 오류 발생: {e}")