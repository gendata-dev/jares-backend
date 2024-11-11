import os

""" 경로 및 기본 설정 """
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FOLDER = os.path.join(BASE_DIR, "log")
CALL_LOG_FOLDER = os.path.join(LOG_FOLDER, "call_log")
SERVER_LOG_FOLDER = os.path.join(LOG_FOLDER, "server_log")
SERVER_LOG_FILE = "logging.log"

""" 로그 포맷 """
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
