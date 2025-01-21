from review_analysis.crawling.base_crawler import BaseCrawler
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

import pandas as pd
import time

class ExampleCrawler(BaseCrawler):
    def __init__(self, output_dir: str):
        super().__init__(output_dir)
        self.base_url = 'https://map.naver.com/p/entry/place/21306384?c=15.00,0,0,0,dh&placePath=/review'
        self.reviews=[]

    def start_browser(self):
        chrome_options = Options()
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(self.base_url)
        print('"파이홀" 네이버 리뷰 페이지 로딩 성공')

    def scrape_reviews(self):
        columns=['content','date','stars']
        values=[]
        soup=BeautifulSoup(self.driver.page_source)
    
    def save_to_database(self):
        pass
