# review_analysis/preprocessing/example_processor.py

import pandas as pd
import os
from review_analysis.preprocessing.base_processor import BaseDataProcessor
from transformers import AutoTokenizer, AutoModel  # type: ignore
import torch
import numpy as np

class KakaoProcessor(BaseDataProcessor):
    """
   카카오맵 리뷰 데이터 전처리 및 특성 공학 클래스

   주요 기능:
   - 결측치 및 불필요한 리뷰 제거
   - 데이터 정규화 및 특성 엔지니어링
   - KcBERT 모델을 사용한 텍스트 벡터화

   Args:
       input_path (str): 입력 CSV 파일 경로
       output_path (str): 출력 파일 저장 경로
       model_name (str, optional): 사용할 언어 모델 이름. 기본값은 'beomi/kcbert-base'
       max_length (int, optional): 토큰 최대 길이. 기본값은 128
       batch_size (int, optional): 벡터화 배치 크기. 기본값은 32
   """
    def __init__(self, input_path: str, output_path: str, model_name: str = 'beomi/kcbert-base', max_length: int = 128, batch_size: int = 32):
        """
        KakaoProcessor 초기화 및 모델 로드

        토크나이저와 언어 모델을 로드하고, GPU 사용 가능 시 모델을 GPU로 이동
        """
        super().__init__(input_path, output_path)
        self.output_path = output_path
        self.data = None  # pandas DataFrame을 저장할 변수
        self.model_name = model_name
        self.max_length = max_length
        self.batch_size = batch_size
        
        # 토크나이저 및 모델 로드
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModel.from_pretrained(self.model_name)
            self.model.eval()
            
            # GPU 사용 가능 시 GPU로 이동
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            self.model.to(self.device)
            print(f"모델 로드 및 디바이스 설정 완료: {self.device}")
        except Exception as e:
            print(f"모델 로드 중 오류 발생: {e}")
            raise e  # 초기화 실패 시 예외 발생

    def preprocess(self):
        """
        데이터 전처리:
        - 리뷰 내용이 없는 리뷰 제거
        - 리뷰 내용이 한 단어만 있는 리뷰 제거
        - 별점이 없는 리뷰 제거
        - 날짜가 없는 리뷰 제거
        - 'text' 값이 '내용 없음'인 리뷰 제거
        - 'date' 열의 구분자를 '.'에서 '-'로 변경
        - 'date' 열의 끝에 있는 '-' 제거
        """
        try:
            # 데이터 로드
            self.data = pd.read_csv(self.input_path, encoding='utf-8')
            print(f"원본 데이터 로드 완료: {len(self.data)}개 리뷰")
    
            # 결측치 제거
            initial_count = len(self.data)
            self.data.dropna(subset=['text', 'rating', 'date'], inplace=True)
            removed_count = initial_count - len(self.data)
            print(f"결측치 제거: {removed_count}개 리뷰 제거, 현재 리뷰 수: {len(self.data)}개")
    
            # 'rating'이 NaN인 경우 제거
            initial_count = len(self.data)
            self.data = self.data[self.data['rating'].notna()]
            removed_no_rating = initial_count - len(self.data)
            print(f"별점이 없는 리뷰 제거: {removed_no_rating}개 리뷰 제거, 현재 리뷰 수: {len(self.data)}개")
    
            # 리뷰 내용이 한 단어만 있는 경우 제거
            initial_count = len(self.data)
            self.data = self.data[self.data['text'].apply(lambda x: len(str(x).split()) > 1)]
            removed_one_word_count = initial_count - len(self.data)
            print(f"한 단어 리뷰 제거: {removed_one_word_count}개 리뷰 제거, 현재 리뷰 수: {len(self.data)}개")
    
            # 'text' 값이 '내용 없음'인 리뷰 제거
            initial_count = len(self.data)
            self.data = self.data[self.data['text'] != '내용 없음']
            removed_no_content = initial_count - len(self.data)
            print(f"'내용 없음' 리뷰 제거: {removed_no_content}개 리뷰 제거, 현재 리뷰 수: {len(self.data)}개")
    
            # 'date' 열의 구분자를 '.'에서 '-'로 변경
            if 'date' in self.data.columns:
                self.data['date'] = self.data['date'].str.replace('.', '-', regex=False)
                print(f"'date' 열의 구분자를 '.'에서 '-'로 변경 완료.")
            else:
                print(f"'date' 열이 존재하지 않습니다. 구분자 변경을 건너뜁니다.")
    
            # 'date' 열의 끝에 있는 '-' 제거
            if 'date' in self.data.columns:
                self.data['date'] = self.data['date'].str.rstrip('-')
                print(f"'date' 열의 끝에 있는 '-' 제거 완료.")
            else:
                print(f"'date' 열이 존재하지 않습니다. '-' 제거를 건너뜁니다.")
    
        except FileNotFoundError:
            print(f"파일을 찾을 수 없습니다: {self.input_path}")
        except pd.errors.EmptyDataError:
            print("빈 파일이거나 데이터가 없습니다.")
        except Exception as e:
            print(f"전처리 중 오류 발생: {e}")
    
    def feature_engineering(self):
        """
        특성 엔지니어링:
        - 별점이 0점 미만 또는 5점을 초과하는 리뷰 제거
        - 별점이 정수가 아닌 리뷰 제거
        - 리뷰 작성 월을 나타내는 'month' 컬럼 추가
        - 텍스트 데이터를 KcBERT를 이용하여 벡터화
        """
        try:
            initial_count = len(self.data)
    
            # 별점이 0점 미만 또는 5점을 초과하는 리뷰 제거
            self.data = self.data[(self.data['rating'] >= 0) & (self.data['rating'] <= 5)]
            after_range_filter_count = len(self.data)
            removed_range_count = initial_count - after_range_filter_count
            print(f"별점 범위 필터링: {removed_range_count}개 리뷰 제거, 현재 리뷰 수: {len(self.data)}개")
    
            # 별점이 정수가 아닌 리뷰 제거
            initial_count = len(self.data)
            self.data = self.data[self.data['rating'] == self.data['rating'].astype(int)]
            after_integer_filter_count = len(self.data)
            removed_integer_count = initial_count - after_integer_filter_count
            print(f"별점 정수 필터링: {removed_integer_count}개 리뷰 제거, 현재 리뷰 수: {len(self.data)}개")
    
            # 'rating'을 정수형으로 변환
            self.data['rating'] = self.data['rating'].astype(int)
    
            # 'month' 컬럼 추가
            initial_count = len(self.data)
            # 날짜 형식이 'YYYY-MM-DD'로 변경되었으므로, 이를 기준으로 월 추출
            self.data['month'] = pd.to_datetime(self.data['date'], format='%Y-%m-%d', errors='coerce').dt.month
            # 날짜 변환 실패한 경우 NaT가 생기므로, 'month'가 NaN인 리뷰 제거
            self.data.dropna(subset=['month'], inplace=True)
            # 'month'를 정수형으로 변환
            self.data['month'] = self.data['month'].astype(int)
            after_month_filter_count = len(self.data)
            removed_month_count = initial_count - after_month_filter_count
            print(f"'month' 추가 후 결측치 제거: {removed_month_count}개 리뷰 제거, 현재 리뷰 수: {len(self.data)}개")
    
            # 텍스트 데이터를 벡터화하여 새로운 컬럼 'vector' 추가
            texts = self.data['text'].tolist()
            vectors = self.vectorize_texts(texts)
            self.data['vector'] = vectors.tolist()  # 각 벡터를 리스트 형태로 저장
            print(f"텍스트 데이터 벡터화 완료. 'vector' 컬럼 추가.")
    
        except AttributeError:
            print("데이터가 로드되지 않았거나 올바르게 전처리되지 않았습니다.")
        except Exception as e:
            print(f"특성 엔지니어링 중 오류 발생: {e}")
    
    def vectorize_texts(self, texts):
        """
            텍스트를 KcBERT 모델을 사용하여 벡터화

            Args:
                texts (List[str]): 벡터화할 텍스트 리스트

            Returns:
                numpy.ndarray: 벡터화된 텍스트 임베딩
        """
        all_embeddings = []
        try:
            for i in range(0, len(texts), self.batch_size):
                batch_texts = texts[i:i+self.batch_size]
                # 토큰화
                inputs = self.tokenizer(batch_texts, return_tensors='pt', max_length=self.max_length, truncation=True, padding='max_length')
                inputs = {key: val.to(self.device) for key, val in inputs.items()}
                
                with torch.no_grad():
                    outputs = self.model(**inputs)
                
                # [CLS] 토큰의 임베딩을 사용
                cls_embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy()
                all_embeddings.append(cls_embeddings)
            
            # 모든 배치의 임베딩을 결합
            all_embeddings = np.concatenate(all_embeddings, axis=0)
            return all_embeddings
        except Exception as e:
            print(f"텍스트 벡터화 중 오류 발생: {e}")
            return np.array([])  # 빈 배열 반환
    
    def save_to_database(self):
        """
        전처리된 데이터를 CSV 파일로 저장:
        - 저장 경로: database/preprocessed_reviews_<사이트 이름>.csv
        """
        try:
            # 출력 파일 경로 설정
            base_name = os.path.splitext(os.path.basename(self.input_path))[0]  # ex: reviews_kakaomap
            output_file = os.path.join(self.output_path, f"preprocessed_{base_name}.csv")
    
            # 출력 디렉토리가 존재하지 않으면 생성
            output_dir = os.path.dirname(output_file)
            os.makedirs(output_dir, exist_ok=True)
    
            # 데이터 저장
            self.data.to_csv(output_file, index=False, encoding='utf-8')
            print(f"전처리된 데이터가 저장되었습니다: {output_file}")
    
        except Exception as e:
            print(f"데이터 저장 중 오류 발생: {e}")
