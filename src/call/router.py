from fastapi import APIRouter

from call.service import CallStarter, AnswerHandler, QuestionPreparer, CallEnder
from call.schema import CallDetailRecord, AnswerRecord


router = APIRouter()
""" BASE_URL/v1 """


@router.post("/calls")
async def post_call():
    """
    통화 시작 시 호출
    """
    return await CallStarter.start_call()


@router.post("/answer")
async def handle_answer(answer_data: AnswerRecord):
    """
    수신 응답 받은 경우 호출
    """
    return await AnswerHandler.handle_answer(answer_data)


@router.post("/hangup")
async def hangup_call(call_record: CallDetailRecord):
    """
    통화 종료 시 호출
    TODO: 통화에 관한 정보들을 반환할 필요가 있는지? S3?
    """
    return await CallEnder.end_call(call_record)


@router.post("/talk")
async def handle_talk():
    """
    질문과 답변의 상호작용
    대화 요청을 처리한다
    """
    return await QuestionPreparer.prepare_next_question()
