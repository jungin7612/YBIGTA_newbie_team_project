# 🛠️ 베이스라인즈 (BaseLines)팀 팀원 자기소개 🛠️

---

## 🐍 김현운

- **학과:** 응용통계학과 23학번
- **지원:** DA
- **자기소개:**  
  백준을 한 문제도 풀어보지 않았던 코린이지만, 앞으로 열심히 노력하여 팀에 도움이 되고자 합니다!  
  방학 스터디에서는 **시각화**와 **교육세션 복습**을 신청했습니다.
  - **교육세션 복습:** 첫 수업에서 느낀 어려움을 극복하고자 신청.
  - **시각화:** 태블로와 맷플롯립(Matplotlib)을 통해 데이터와 분석 결과를 시각화하는 기술을 배우고 싶습니다.
- **각오:** 부족하지만 열심히 공부해서 팀에 누가 되지 않도록 따라잡겠습니다!

---

## ⚾ 성우제

- **학과:** 산업공학과 19학번
- **지원:** DA
- **자기소개:**  
  데이터 분석가로서의 커리어를 목표로 DA팀에 지원했습니다.  
  팀원들과 함께 성장하며 데이터 분석 역량을 키우고 싶습니다!
  - **특이사항:** 야구를 굉장히 좋아합니다. 🧢⚾
- **각오:** DA팀 활동을 통해 데이터 분석의 기초를 탄탄히 다지고 싶습니다.

---

## 🎸 김정인

- **학과:** 컴퓨터과학과 24학번
- **지원:** DE, DS (공동 1순위)
- **자기소개:**  
  다양한 경험을 하고 싶어 DE와 DS 분야에 공동 지원했습니다.
  - **취미:** 야구 ⚾, 축구 ⚽, 락뮤직 🎵
- **각오:** 팀 활동을 통해 다양한 지식과 기술을 배우고, 성장의 발판을 마련하고 싶습니다.

---

### 🙌 함께 성장하는 베이스라인즈 (BaseLines)팀이 되길 기대합니다!

<div style="display: flex; justify-content: center; align-items: center; gap: 20px;">
    <img src="github/branch_protection.png" height="120px" width="150px">
    <img src="github/merged_jungin7612.png" height="120px" width="150px">
    <img src="github/merged_SungWoojae.png" height="120px" width="150px">
    <img src="github/merged_yonseistatking.png" height="120px" width="150px">
    <img src="github/push_rejected.png" height="120px" width="150px">
</div>

# YBIGTA Newbie Team Project 실행 방법

## 설치 방법

1. **Python 버전 확인**  
   Python 3.7 이상(또는 프로젝트에서 권장하는 버전)을 사용 중인지 확인합니다.

2. **가상 환경(옵션)**  
   원활한 패키지 관리를 위해 가상 환경 사용을 권장합니다.

   ```bash
   # 가상환경 생성 예시
   python -m venv venv
   source venv/bin/activate  # Mac/Linux
   # 또는 venv\Scripts\activate  # Windows

   ```

3. **프로젝트 종속 라이브러리 설치**  
   프로젝트 루트 디렉토리(`YBIGTA_newbie_team_project`)에서 다음 명령어를 실행합니다.
   ```bash
   pip install -r requirements.txt
   ```
4. 실행 방법
   **Uvicorn을 사용한 실행**  
   가장 간단한 실행 방법은 uvicorn 명령어를 이용하는 것입니다.
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```
   - `app.main:app`은 `app` 폴더 내부의 `main.py`에서 FastAPI 인스턴스가 `app`이라는 이름으로 선언되어 있음을 가정합니다.
   - `--reload`는 개발 편의를 위해 코드 변경 시 자동으로 서버를 재시작합니다.
   - `--host`와 `--port`는 원하는 IP 주소와 포트를 지정할 수 있습니다(기본은 `127.0.0.1:8000`).

## KaKao EDA

<div style="display: flex; justify-content: center; align-items: center; gap: 20px;">
   <img src="review_analysis/plots/rating_distribution.png" height="300px" width="600px">
   <img src="review_analysis/plots/reivew_text_length_dtb.png" height="300px" width="600px">
</div>
<img src="review_analysis/plots/outlier.png" height="256 px" width="1076px">
분석 결과를 바탕으로 데이터의 특성과 이상치에 대해 설명드리겠습니다:

1. Rating (평점) 특성:

- 총 377개의 평점 데이터 존재
- 평균 평점은 약 4.09점으로 상당히 높은 수준
- 표준편차는 1.09로 평점의 변동성이 크지 않음
- 평점 분포는 4점에 집중되어 있음 (25%, 50% 모두 4점)
- 최소 1점에서 최대 5점까지 분포
- 대부분의 리뷰가 4-5점 사이에 집중되어 있어 긍정적인 평가가 많음

2. 리뷰 길이 특성:

- 총 377개의 리뷰 길이 데이터
- 평균 리뷰 길이는 약 50자
- 표준편차가 65.67로 리뷰 길이의 편차가 큼
- 최소 2자에서 최대 480자까지 wide range
- 중앙값(50%)은 29자로, 대부분의 리뷰는 상대적으로 짧은 편
- 리뷰 길이 분포가 매우 비대칭적

3. 이상치 분석:

- Rating 이상치: 없음
- 리뷰 길이 이상치: 10개 존재
- Date 이상치: 없음

4. 날짜 범위:

- 최소 날짜: 2016-04-07
- 최대 날짜: 2025-01-13 (미래 날짜 포함)

주목할 만한 점:

- 리뷰 길이의 높은 표준편차는 리뷰 길이가 매우 다양함을 의미
- 10개의 리뷰 길이 이상치는 추가 조사가 필요할 수 있음

## Kakao 전처리/FE

1. 결측치 처리:

- 초기 리뷰 수에서 결측치 제거
- 'text', 'rating', 'date' 열의 결측치 제거
- '내용 없음' 리뷰 제거
- 한 단어로 된 리뷰 제거

2. 이상치 및 데이터 정제:

- 별점 범위 필터링 (0~5점)
- 별점 정수형 변환
- 날짜 형식 통일 ('.'->'-)
- 날짜 끝 '-' 제거

3. 텍스트 데이터 전처리:

- KcBERT 모델 사용
- 텍스트 토큰화 (최대 길이 128)
- [CLS] 토큰 임베딩 추출

4. 파생변수 생성:

- 'month' 컬럼 추가 (리뷰 작성 월)
- 'vector' 컬럼 추가 (텍스트 벡터화 결과)

5. 벡터화 방식:

- 배치 처리 (배치 크기: 32)
- GPU 사용 (가능한 경우)
- 벡터 길이: 모델 은닉층 차원

최종 결과: 정제된 리뷰 데이터셋 생성, CSV 파일로 저장
