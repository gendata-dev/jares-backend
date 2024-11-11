import os
import logging
from fastapi import FastAPI

from auth.router import router as auth_router
from call.router import router as call_router

from constant import (
    LOG_FOLDER,
    SERVER_LOG_FOLDER,
    CALL_LOG_FOLDER,
    SERVER_LOG_FILE,
    LOG_FORMAT,
    DATE_FORMAT,
)


app = FastAPI()

""" 라우터 추가 """
app.include_router(auth_router, prefix="/user-management", tags=["auth"])
app.include_router(call_router, prefix="/v1", tags=["call"])


@app.on_event("startup")
def startup_event():
    """서버 로그 폴더와 통화 로그 폴더 생성"""
    os.makedirs(LOG_FOLDER, exist_ok=True)
    os.makedirs(SERVER_LOG_FOLDER, exist_ok=True)
    os.makedirs(CALL_LOG_FOLDER, exist_ok=True)

    server_log_file = os.path.join(SERVER_LOG_FOLDER, SERVER_LOG_FILE)

    logging.basicConfig(
        filename=server_log_file,
        level=logging.INFO,
        format=LOG_FORMAT,
        datefmt=DATE_FORMAT,
    )
