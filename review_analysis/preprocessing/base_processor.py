from abc import ABC, abstractmethod

class BaseDataProcessor:
    def __init__(self, input_path: str, output_dir: str):
        self.input_path = input_path
        self.output_dir = output_dir
    
    @abstractmethod
    def preprocess(self):
        pass
    
    @abstractmethod
    def feature_engineering(self):
        pass

    @abstractmethod
    def vectorize_text(self, text_series):
        """텍스트 데이터를 벡터화하는 메서드 (하위 클래스에서 구현)"""
        pass
    
    @abstractmethod
    def save_to_database(self):
        
        pass


