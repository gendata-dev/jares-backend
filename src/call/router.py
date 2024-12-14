from fastapi import APIRouter, Depends

from src.call.service import (
    CallStartService,
    AnswerHandleService,
    QuestionPrepareService,
    CallEndService,
)
from src.call.schema import CallDetailRecord, AnswerRecord, TalkRecord

router = APIRouter()
""" BASE_URL/v1 """


@router.post("/calls")
def post_call():
    """
    통화 시작 시 호출
    """
    return CallStartService()


@router.post("/answer")
def handle_answer(
    answer_record: AnswerRecord,
    service: AnswerHandleService = Depends(AnswerHandleService),
):
    """
    수신 응답 받은 경우 호출
    """
    return service.handle_answer(answer_record)


@router.post("/hangup")
def hangup_call(
    call_record: CallDetailRecord, service: CallEndService = Depends(CallEndService)
):
    """
    통화 종료 시 호출
    TODO: 통화에 관한 정보들을 반환할 필요가 있는지? S3?
    """
    return service.end_call(call_record)


@router.post("/talk")
def handle_talk(
    talk_record: TalkRecord,
    service: QuestionPrepareService = Depends(QuestionPrepareService),
):
    """
    질문과 답변의 상호작용
    대화 요청을 처리한다
    """
    return service.prepare_sentence(talk_record)
