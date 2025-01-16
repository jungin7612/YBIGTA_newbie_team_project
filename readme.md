# 🛠️ 팀 팀원 자기소개 🛠️

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

### 🙌 함께 성장하는 DA팀이 되길 기대합니다!

<img src="./github/branch_protected.png", height="100px", width="100px">
<img src="./github/merged_jungin7612.png", height="100px", width="100px">
<img src="./github/merged_SungWoojae.png", height="100px", width="100px">
<img src="./github/merged_yonseistatking.png", height="100px", width="100px">
<img src="./github/push_rejected.png", height="100px", width="100px">

아래는 해당 프로젝트를 로컬 환경에서 실행하기 위한 절차입니다:

markdown
코드 복사
# YBIGTA Newbie Team Project 실행 방법

## 1. 저장소 클론

먼저, 터미널에서 해당 프로젝트를 로컬로 클론합니다:

```bash
git clone https://github.com/jungin7612/YBIGTA_newbie_team_project.git
cd YBIGTA_newbie_team_project
2. 가상 환경 설정
프로젝트의 의존성을 격리하기 위해 가상 환경을 생성하고 활성화합니다:

bash
코드 복사
# 가상 환경 생성
python -m venv venv

# 가상 환경 활성화 (Windows)
venv\Scripts\activate

# 가상 환경 활성화 (macOS/Linux)
source venv/bin/activate
3. 의존성 설치
requirements.txt 파일을 통해 필요한 패키지를 설치합니다:

bash
코드 복사
pip install -r requirements.txt

4. 애플리케이션 실행 (Uvicorn 사용)
FastAPI 애플리케이션을 실행하기 위해 Uvicorn을 사용합니다:

bash
코드 복사
# 서버 실행 명령어
uvicorn app.main:app --reload --host=0.0.0.0 --port=8000
app.main:app은 app 디렉토리의 main.py 파일 내에 정의된 FastAPI 인스턴스를 가리킵니다. 프로젝트 구조에 따라 경로를 조정해야 할 수 있습니다.
--reload 옵션은 코드 변경 시 자동으로 서버를 재시작하도록 합니다. 개발 환경에서 유용합니다.
--host와 --port 옵션은 서버의 호스트와 포트를 지정합니다. 필요에 따라 조정 가능합니다.
이후 웹 브라우저에서 http://localhost:8000으로 접속하여 애플리케이션을 확인할 수 있습니다.