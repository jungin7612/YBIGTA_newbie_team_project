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

class NaverCrawler(BaseCrawler):
    def __init__(self, output_dir: str):
        super().__init__(output_dir)
        self.base_url = 'https://map.naver.com/p/entry/place/21306384?c=15.00,0,0,0,dh&placePath=/review'
        self.reviews=[]
        self.driver=None

    def start_browser(self):
        chrome_options = Options()
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.base_url)
        print('"파이홀" 네이버 리뷰 페이지 로딩 성공')

    def scrape_reviews(self):
        columns=['content','date','stars']
        values=[]
        n=0
        seen_reviews = set() 
        for _ in range(5):
            interval=3
            prev_height=self.driver.execute_script("return document.body.scrollHeight")

            while True:
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                # 페이지 로딩 대기
                time.sleep(interval)

                # 현재 문서 높이를 가져와서 저장
                curr_height = self.driver.execute_script("return document.body.scrollHeight")
                if curr_height == prev_height:
                    break

                prev_height = curr_height

            try:
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.pui__X35jYm.EjjAW'))
                )
                soup=BeautifulSoup(self.driver.page_source,'html.parser')
                reviews=soup.select('li.pui__X35jYm.EjjAW')

                if not reviews:
                    print("리뷰 조회 실패.")
                    break

                for review in reviews:
                    n+=1
                    print(f"{n}번째 리뷰 크롤링")
                    blank=[]
                    try:
                        content_tag = review.find('a', attrs={'data-pui-click-code': 'rvshowmore'})
                        content = content_tag.text.strip() if content_tag else None
                        if content and content not in seen_reviews:
                            seen_reviews.add(content)
                            blank.append(content)

                    except Exception as e:
                        print(f"{n}번째 리뷰 내용 가져오는 중에 오류 발생",e)
                        blank.append("Error")
                        continue
                    
                    try:
                        date_tag = review.find('time')
                        date = date_tag.text.strip() if date_tag else "날짜 없음"
                        blank.append(date)
                    except Exception as e:
                        print(f"{n}번째 리뷰 날짜 가져오는 중에 오류 발생",e)
                        blank.append("Error")
                        continue
                    try:
                        '''
                        별점가져와야함
                        '''
                        blank.append(f"{n}번째 리뷰 별점")
                    except Exception as e:
                        pass

                    values.append(blank)
                    print('------------------------------------------------------')
                try:
                    more_button = WebDriverWait(self.driver, 20).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '//*[@id="app-root"]/div/div/div/div[6]/div[3]/div[3]/div[2]/div/a')
                        )
                    )
                    more_button.click()
                    time.sleep(5)
                except Exception as e:
                    print("더보기 버튼이 없거나 클릭 실패:", e)
                    break
            except Exception as e:
                print("리뷰 크롤링 중에 오류 발생:", e)
                break

        if values:    
            df=pd.DataFrame(values,columns=columns)
            self.reviews.append(df)
            print("크롤링 완료")
        else:
            print("크롤링 데이터 없음")

    
    def save_to_database(self):
        if not self.reviews:
            print("저장할 리뷰 데이터가 없습니다. 크롤링 데이터를 확인하세요.")
            return
    
        try:
            # 리뷰 데이터를 하나의 DataFrame으로 병합
            final_df = pd.concat(self.reviews, ignore_index=True)
            
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)  # 디렉토리 생성
            output_path = os.path.join(self.output_dir, "reviews.csv")

            # 지정된 경로에 파일 저장
            final_df.to_csv(output_path, index=False, encoding='utf-8-sig')             
            print(f"리뷰 데이터가 성공적으로 저장되었습니다: {output_path}")
        except Exception as e:
            print(f"데이터 저장 중 오류 발생: {e}")
