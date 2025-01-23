# 필요한 패키지 로딩
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 데이터 불러오기
file_path = 'C:/Users/kimhy/OneDrive/Documents/YBIGTA/3주차_250114/크롤링/database/reviews_googlemaps.csv'  # 파일 경로를 적절히 변경하세요
df = pd.read_csv(file_path)

# 데이터 기본 정보 확인
print("데이터프레임 정보:")
df.info()
print("\n데이터 샘플:")
print(df.head())

# 별점 분포 파악
df['별점'] = pd.to_numeric(df['별점'], errors='coerce')
print("\n별점 통계 요약:")
print(df['별점'].describe())

# 리뷰 텍스트 길이 분석
df['리뷰_길이'] = df['리뷰 내용'].astype(str).apply(len)
print("\n리뷰 길이 통계 요약:")
print(df['리뷰_길이'].describe())

# 날짜 분포 파악
df['날짜'] = pd.to_datetime(df['날짜'], errors='coerce')
print("\n날짜 범위:")
print(f"최소 날짜: {df['날짜'].min()}, 최대 날짜: {df['날짜'].max()}")

# 이상치 파악 (별점 범위, 리뷰 길이, 날짜 범위)
rating_outliers = df[(df['별점'] < 1) | (df['별점'] > 5)]
text_length_outliers = df[(df['리뷰_길이'] < 5) | (df['리뷰_길이'] > 1000)]
date_outliers = df[(df['날짜'] < '2000-01-01') | (df['날짜'] > pd.Timestamp.now())]

print("\n이상치 개수:")
print(f"별점 이상치: {len(rating_outliers)}")
print(f"리뷰 길이 이상치: {len(text_length_outliers)}")
print(f"날짜 이상치: {len(date_outliers)}")

# 시각화: 별점과 리뷰 길이 분포
plt.figure(figsize=(12, 6))
sns.histplot(df['별점'].dropna(), bins=20, kde=True)
plt.title('별점 분포')
plt.xlabel('별점')
plt.ylabel('빈도')
plt.show()

plt.figure(figsize=(12, 6))
sns.histplot(df['리뷰_길이'], bins=50, kde=True)
plt.title('리뷰 텍스트 길이 분포')
plt.xlabel('리뷰 길이(글자 수)')
plt.ylabel('빈도')
plt.show()
