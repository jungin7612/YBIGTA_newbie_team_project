from review_analysis.preprocessing.base_processor import BaseDataProcessor
import pandas as pd
import os
from transformers import AutoTokenizer, AutoModel # type: ignore
import torch

class NaverProcessor(BaseDataProcessor):
    def __init__(self, input_path: str, output_path: str):
        """
        NaverProcessor 초기화 메서드.

        Args:
            input_path (str): 입력 파일 경로.
            output_path (str): 출력 파일 저장 경로.
        """
        super().__init__(input_path, output_path)
        self.file_path: str = input_path
        self.output_path: str = output_path
        self.processed_df_with_stars: pd.DataFrame | None = None
        self.processed_df_without_stars: pd.DataFrame | None = None

        # KC-BERT 모델과 토크나이저 로드
        self.model_name: str = "beomi/kcbert-base"
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.model = AutoModel.from_pretrained(self.model_name)
        self.device: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def preprocess(self) -> None:
        """
        데이터를 전처리합니다.
        """
        df: pd.DataFrame = pd.read_csv(self.file_path)

        # 결측치 처리
        print("----------------------결측치 처리 시작----------------------")
        df_content_cleaned: pd.DataFrame = df.dropna(subset=['text'])
        print(f"리뷰 내용이 없어서 삭제한 리뷰 개수: {df['text'].isnull().sum()}")
        print(f"리뷰내용이 없는 리뷰 개수: {df_content_cleaned['text'].isnull().sum()}")

        df_with_stars: pd.DataFrame = df_content_cleaned.dropna(subset=['rating'])
        df_without_stars: pd.DataFrame = df_content_cleaned[df_content_cleaned['rating'].isnull()]
        print("별점이 없는 리뷰들:")
        print(df_without_stars.head())
        print("별점이 있는 리뷰들:")
        print(df_with_stars.head())

        df_date_cleaned_with_stars: pd.DataFrame = df_with_stars.dropna(subset=['date'])
        df_date_cleaned_without_stars: pd.DataFrame = df_without_stars.dropna(subset=['date'])
        print(f"날짜가 없어서 삭제한 리뷰 개수: \n (별점 없는 리뷰에서){df_with_stars['date'].isnull().sum()} \n (별점 있는 리뷰에서){df_without_stars['date'].isnull().sum()}")

        print("-----------------------------------------------------------")
        print("별점 있는 리뷰들:")
        print(df_date_cleaned_with_stars)
        print("-----------------------------------------------------------")
        print("별점 없는 리뷰들:")
        print(df_date_cleaned_without_stars)
        print("----------------------결측치 처리 완료----------------------")

        # 이상치 처리
        print("----------------------이상치 처리 시작----------------------")
        df_date_cleaned_with_stars = df_date_cleaned_with_stars[(df_date_cleaned_with_stars['rating'] >= 0) & 
                                                                (df_date_cleaned_with_stars['rating'] <= 5)]
        print(f"별점이 0 미만이거나 5를 초과하여 삭제된 리뷰 개수: {(df_date_cleaned_with_stars['rating'] < 0).sum() + (df_date_cleaned_with_stars['rating'] > 5).sum()}")
        self.processed_df_with_stars = df_date_cleaned_with_stars[df_date_cleaned_with_stars['text'].str.split().str.len() > 1]
        self.processed_df_without_stars = df_date_cleaned_without_stars[df_date_cleaned_without_stars['text'].str.split().str.len() > 1]
        print(f"별점 있는 리뷰 중 삭제된 행 개수 (단어 수 1개 이하): {len(df_date_cleaned_with_stars) - len(self.processed_df_with_stars)}")
        print(f"별점 없는 리뷰 중 삭제된 행 개수 (단어 수 1개 이하): {len(df_date_cleaned_without_stars) - len(self.processed_df_without_stars)}")
        print("----------------------이상치 처리 완료----------------------")

        print("[데이터 전처리 완료]")

    def feature_engineering(self) -> None:
        """
        피처 엔지니어링 수행.
        """
        print("[FE 시작]")

        if self.processed_df_with_stars is not None:
            self.processed_df_with_stars['month'] = self.processed_df_with_stars['date'].apply(
                lambda x: int(str(x).split('-')[1]) if '-' in str(x) else None
            )

        if self.processed_df_without_stars is not None:
            self.processed_df_without_stars['month'] = self.processed_df_without_stars['date'].apply(
                lambda x: int(str(x).split('-')[1]) if '-' in str(x) else None
            )

        print("별점 있는 리뷰 데이터프레임에 month 열 추가 완료:")
        if self.processed_df_with_stars is not None:
            print(self.processed_df_with_stars[['date', 'month']].head())
        print("별점 없는 리뷰 데이터프레임에 month 열 추가 완료:")
        if self.processed_df_without_stars is not None:
            print(self.processed_df_without_stars[['date', 'month']].head())

        print("[텍스트 벡터화 시작]")
        if self.processed_df_with_stars is not None:
            self.processed_df_with_stars['vector'] = self.vectorize_text(self.processed_df_with_stars['text'])
        if self.processed_df_without_stars is not None:
            self.processed_df_without_stars['vector'] = self.vectorize_text(self.processed_df_without_stars['text'])
        print("[텍스트 벡터화 완료]")

        print("[FE 완료]")

    def vectorize_text(self, text_series: pd.Series) -> list:
        """
        KC-BERT를 이용해 텍스트를 벡터화합니다.
        """
        vectors: list = []

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

    def save_to_database(self) -> None:
        """
        처리된 데이터프레임을 CSV 파일로 저장합니다.
        """
        print("[CSV 저장 시작]")

        if self.processed_df_with_stars is not None:
            with_stars_path = os.path.join(self.output_path, "processed_reviews_naver.csv")
            self.processed_df_with_stars.to_csv(with_stars_path, index=False, encoding="utf-8-sig")
            print(f"별점 있는 리뷰 데이터가 저장되었습니다: {with_stars_path}")
        else:
            print("processed_reviews_naver가 None입니다. 저장하지 않습니다.")

        if self.processed_df_without_stars is not None:
            without_stars_path = os.path.join(self.output_path, "processed_reviews_without_stars_for_testing.csv")
            self.processed_df_without_stars.to_csv(without_stars_path, index=False, encoding="utf-8-sig")
            print(f"별점 없는 리뷰 데이터가 저장되었습니다: {without_stars_path}")
        else:
            print("processed_reviews_without_stars_for_testing가 None입니다. 저장하지 않습니다.")

        print("[CSV 저장 완료]")
