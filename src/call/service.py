import os
import csv
import logging
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from call.schema import CallDetailRecord, AnswerRecord

from constant import CALL_LOG_FOLDER


"""
각 농가에 전화를 걸어서 농업 관련 조사를 진행한다
발신: 서버
수신: 농가

통화의 플로우
발신 -> 수신 대기 -> 수신 -> 대화 -> 종료
    -> dial -> answer -> talk -> hangup
"""
# TODO: response가 지저분하다
class AnswerHandler:
    """ 수신 응답 시 호출 """

    # TODO: 데이터 보관? 로그의 내용이 부족하진 않은지? 전화번호 추가 등등
    @classmethod
    async def handle_answer(cls, answer_data: AnswerRecord):
        logging.info(
                "Answer received."
                + " Call ID: "
                + answer_data.get("call_id")
                + " Answer Time: "
                + answer_data.get("answer_time")
                + " Direction: "
                + answer_data.get("direction")
            )
        
        return JSONResponse(content={
            "response_message": {
                "code": "0000",
                "message": "success",
            }
        })


class CallStarter:
    async def start_call(cls):
        print("Starting call")


class QuestionPreparer:
    async def prepare_next_question(cls, call_id: str):
        print(f"Preparing next question for call {call_id}")


class CallEnder:
    """ 전화 종료 시 호출 """

    @classmethod
    async def end_call(cls, call_record: CallDetailRecord):
        """ 전화 기록을 csv 파일로 기록 """
        await cls.store_csv_file(call_record)

        return JSONResponse(
            content={
                "status": "success",
                "message": "Hangup request processed",
            })

    @classmethod
    async def store_csv_file(cls, call_record: CallDetailRecord):
        """
        csv 파일을 저장하는 함수
        프로젝트의 경로에 /call_log 디렉토리에
        <call_id>.csv 파일을 생성함

        call_id는 unique한 uuid4 값
        같은 이름의 파일이 생기지 않음
        
        드물게 같은 이름의 파일이 생길 경우
        값을 덮어씌운다
        """
        call_id = call_record.get("call_id")
        file_path = os.path.join(CALL_LOG_FOLDER, f"{call_id}.csv")

        if not os.path.exists(CALL_LOG_FOLDER):
            logging.error(f"Directory was deleted {CALL_LOG_FOLDER}")
            os.makedirs(CALL_LOG_FOLDER)

        try:
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(call_record.keys())
                writer.writerow(call_record.values())

        # TODO: make exeception or not raised exception, return response
        except PermissionError:
            logging.error(f"Permission denied {file_path}")
            raise HTTPException(
                status_code=403,
                detail="Permission denied: Unable to write to the file at the specified path."
            )
        except FileNotFoundError:
            logging.error(f"File not found {file_path}")
            raise HTTPException(
                status_code=404,
                detail="File path not found or the directory does not exist."
            )
        except OSError as e:
            logging.error(f"OSError {file_path}: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"An unexpected error occurred: {e.strerror}"
            )