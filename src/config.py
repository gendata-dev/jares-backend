import os
from starlette.config import Config

config = Config(".env")


class LogConfig:
    """경로 및 기본 설정"""

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    LOG_FOLDER = os.path.join(BASE_DIR, "log")
    CALL_LOG_FOLDER = os.path.join(LOG_FOLDER, "call_log")
    SERVER_LOG_FOLDER = os.path.join(LOG_FOLDER, "server_log")
    SERVER_LOG_FILE = "logging.log"

    """ 로그 포맷 """
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class DBConfig:
    """DB 정보"""

    """
    TODO
    아래의 내용을 추가할 경우 Secret 값들을 출력하지 않을 수 있지만 
    공수가 들어서 아직 결정하지 못함

    CREDENTIALS = config("DATABASE_CREDENTIALS", cast=Secret)
    _CREDENTIAL_USER, _CREDENTIAL_PASSWORD = str(CREDENTIALS).split(":")
    _QUOTED_DATABASE_PASSWORD = parse.quote(str(_CREDENTIAL_PASSWORD))
    """
    HOSTNAME = config("DATABASE_HOSTNAME", default="localhost")
    NAME = config("DATABASE_NAME", default="postgres")
    PORT = config("DATABASE_PORT", default="5432")
    USER = config("DATABASE_USER", default="postgres")
    PASSWORD = config("DATABASE_PASSWORD", default="123")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOSTNAME}:{PORT}/{NAME}"
    )
    ENGINE_POOL_SIZE = config("DATABASE_ENGINE_POOL_SIZE", cast=int, default=20)
    ENGINE_MAX_OVERFLOW = config("DATABASE_ENGINE_MAX_OVERFLOW", cast=int, default=0)
