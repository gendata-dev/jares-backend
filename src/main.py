import os
import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.call.router import router as call_router
from src.auth.router import router as auth_router
from src.group.router import router as group_router
from src.survey.router import router as survey_router
from src.contact.router import router as contact_router
from src.routine.router import router as routine_router
from src.question.router import router as question_router
from src.language_model.router import router as language_model_router

from src.config import LogConfig
from src.database import connect_db, disconnect_db


app = FastAPI()

""" 라우터 추가 """
app.include_router(call_router, prefix="/v1", tags=["call"])
app.include_router(auth_router, prefix="/user-management", tags=["auth"])
app.include_router(group_router, prefix="/contact-management", tags=["group"])
app.include_router(contact_router, prefix="/contact-management", tags=["contact"])
app.include_router(survey_router, prefix="/survey-management", tags=["survey"])
app.include_router(question_router, prefix="/question-management", tags=["question"])
app.include_router(routine_router, prefix="/routine-management", tags=["routine"])
app.include_router(
    language_model_router, prefix="/llm-management", tags=["language_model"]
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_log_environment()
    connect_db()
    yield
    disconnect_db()


def setup_log_environment():
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


app.router.lifespan_context = lifespan
