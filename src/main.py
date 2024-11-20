import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

from auth.router import router as auth_router
from call.router import router as call_router
from contact.router import router as contact_router
from routine.router import router as routine_router
from survey.router import router as survey_router

from config import LogConfig


def startup_event():
    """서버 로그 폴더와 통화 로그 폴더 생성"""
    os.makedirs(LogConfig.LOG_FOLDER, exist_ok=True)
    os.makedirs(LogConfig.SERVER_LOG_FOLDER, exist_ok=True)
    os.makedirs(LogConfig.CALL_LOG_FOLDER, exist_ok=True)

    server_log_file = os.path.join(
        LogConfig.SERVER_LOG_FOLDER, LogConfig.SERVER_LOG_FILE
    )

    logging.basicConfig(
        filename=server_log_file,
        level=logging.INFO,
        format=LogConfig.LOG_FORMAT,
        datefmt=LogConfig.DATE_FORMAT,
    )


@asynccontextmanager
async def lifespan(app: FastAPI):
    startup_event()
    yield


app = FastAPI(lifespan=lifespan)

""" 라우터 추가 """
app.include_router(auth_router, prefix="/user-management", tags=["auth"])
app.include_router(contact_router, prefix="/contact-management", tags=["contact"])
app.include_router(routine_router, prefix="/routine-management", tags=["routine"])
app.include_router(survey_router, prefix="/survey-management", tags=["survey"])
app.include_router(call_router, prefix="/v1", tags=["call"])
