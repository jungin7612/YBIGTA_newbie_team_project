from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from app.user.user_router import user
from app.config import PORT
from fastapi.middleware.cors import CORSMiddleware

'''
rejected test용용 third try

이번에는 될 것인가
'''

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 허용할 도메인 리스트
    allow_credentials=True,
    allow_methods=["*"],  # 모든 메서드 허용
    allow_headers=["*"],  # 모든 헤더 허용
)

static_path = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_path), name="static")

app.include_router(user)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)
