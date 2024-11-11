import os

from call.repository import CallRepository, CallDictRepository


class RepositoryConfig:
    REPOSITORY_TYPE = repo_type = os.getenv(
        "REPOSITORY_TYPE"
    )  # 환경 변수나 설정 파일에서 로드할 수 있음

    @classmethod
    def get_call_repository(cls) -> CallRepository:
        # FOR TEST
        print("call_repository called")
        if cls.REPOSITORY_TYPE == "sql":
            print("CALLREPO MAKE")
            return CallRepository()
        else:
            print("CALLDICTREPO MAKE")
            return CallDictRepository()


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
