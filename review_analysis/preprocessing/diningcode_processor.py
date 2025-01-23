from review_analysis.preprocessing.base_processor import BaseDataProcessor
import pandas as pd
from transformers import AutoTokenizer, AutoModel
import torch

class DiningCodeProcessor(BaseDataProcessor):
    def __init__(self, input_path: str, output_path: str):
        super().__init__(input_path, output_path)
        self.df_clean = None  # 인스턴스 변수 초기화
        self.tokenizer = AutoTokenizer.from_pretrained("beomi/kcbert-base")
        self.model = AutoModel.from_pretrained("beomi/kcbert-base")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
    
    def preprocess(self):
        file_path = './database/reviews_diningcode.csv'  
        df = pd.read_csv(file_path)

        # 리뷰가 '리뷰 없음'이 아닌 경우 필터링
        df_clean = df[df['리뷰 내용'] != '리뷰 없음']
        
        # 한 단어 이상인 리뷰만 남기기
        df_clean = df_clean[df_clean['리뷰 내용'].str.split().str.len() > 1]

        # 별점에서 숫자만 추출 후 정수형 변환
        df_clean['별점'] = df_clean['별점'].astype(str).str.extract(r'(\d+)').astype(float).astype(int)

        # 별점 범위를 벗어난 데이터 필터링
        df_clean = df_clean[(df_clean['별점'] >= 0) & (df_clean['별점'] <= 5)]

        # 특정 날짜 수정
        df_clean.loc[1, '날짜'] = '2025년 01월 02일'
        df_clean.loc[2, '날짜'] = '2025년 01월 18일'

        # 인스턴스 변수로 저장
        self.df_clean = df_clean
        print("Preprocessing 완료, 데이터 크기:", self.df_clean.shape)

    def feature_engineering(self):
        if self.df_clean is None:
            raise ValueError("데이터가 존재하지 않습니다. preprocess()를 먼저 실행하세요.")

        # 날짜 변환 및 월 추출
        self.df_clean['날짜'] = pd.to_datetime(self.df_clean['날짜'], format='%Y년 %m월 %d일', errors='coerce')
        self.df_clean['월'] = self.df_clean['날짜'].dt.month.astype(int)

        # 컬럼 이름 변경 및 순서 조정
        self.df_clean.rename(columns={'날짜': 'date', '별점': 'rating', '월': 'month', '리뷰 내용': 'text'}, inplace=True)
        new_order = ['text', 'date', 'rating', 'month']
        self.df_clean = self.df_clean[new_order]

        # 텍스트 벡터화 수행
        print("[텍스트 벡터화 시작]")
        self.df_clean['vector'] = self.vectorize_text(self.df_clean['text'])
        print("[텍스트 벡터화 완료]")
        print("벡터화된 데이터 예시:", self.df_clean['vector'].iloc[0])

    def vectorize_text(self, text_series: pd.Series) -> list:
        """
        텍스트 데이터를 KC-BERT를 사용하여 벡터화합니다.
        
        Args:
            text_series (pd.Series): 텍스트 데이터 시리즈.
        
        Returns:
            list: 텍스트 벡터의 리스트.
        """
        vectors = []

        for text in text_series:
            tokens = self.tokenizer(
                text,
                padding="max_length",
                truncation=True,
                max_length=128,
                return_tensors="pt"
            ).to(self.device)

            with torch.no_grad():
                outputs = self.model(**tokens)
                cls_vector = outputs.last_hidden_state[:, 0, :].cpu().numpy()
                vectors.append(cls_vector[0])

        return vectors
    
    def save_to_database(self):
        if self.df_clean is None:
            raise ValueError("저장할 데이터가 없습니다. preprocess()와 feature_engineering()을 먼저 실행하세요.")

        output_file = 'preprocessed_reviews_diningcode.csv'
        self.df_clean.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"데이터가 {output_file}에 저장되었습니다.")
