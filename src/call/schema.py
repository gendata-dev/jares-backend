from sqlalchemy import Column, Integer, ForeignKey, JSON, TIMESTAMP, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing_extensions import TypedDict
from uuid import uuid4
from enum import Enum as PyEnum

from src.schema import TableBase


"""
call_id	string	call unique id
t_id	string	t id
caller	string	발신번호
callee	string	수신번호
start_time	string	dial 시작 시간
answer_time	string	통화 시작 시간
end_time	string	통화 종료 시간
duration	integer	과금 시간 (초)
dial_duration	integer	전체통화시간 (초) - 다이얼시간 포함
hangup_disposition	string	어디에서(수/발신) 전화를 종료 했는지
cause	string	통화종료 코드
"""


# TODO: use datetime type?
class CallDetailRecord(TypedDict):
    call_id: str
    t_id: str
    caller: str
    callee: str
    start_time: str  # datetime
    answer_time: str  # datetime
    end_time: str  # datetime
    duration: int
    dial_duration: int
    hangup_disposition: str


"""
call_id	string	call unique id		                              uuid4
t_id	string	"dial 전문에서 받은 t_id 없을 경우 call_id와 동일"      미사용	
caller	string	발신번호		                                    0211112222
callee	string	착신번호		                                    01011112222
direction	string	수/발신 구분		                            inbound
answer_time	string	전화 받은 시간		                             2023-01-01 00:00:00
"""


class AnswerRecord(TypedDict):
    call_id: str
    t_id: str
    caller: str
    callee: str
    direction: str
    answer_time: str  # datetime


"""
call_id	    string  call unique id	uuid4	
t_id	    string	t_id	        미사용	
play_status	string	"멘트 재생 상태* barge in 으로 멘트 중지 'break'"	done | break	break
stt	        string	stt 결과		'추천을 하는 게 뭐 좋은 건지 모르겠어요. 이게.'
dtmf	    string	dtmf		1234
dtmf_status	string	"dtmf 수집 상태* 요청한 자리수까지 수집된 경우 'done'"	done | timeout	done
step	    string	테스트 용도 / 무시하셔도 됩니다.	추가	
stt_detail	string	stt 결과 상세		"[
		{
			"start": 0,
			"end": 5688,
			"text": "추천을 하는 게 뭐 좋은 건지 모르겠어요. 이게.",
			"confidence": 0.9725,
			"diarization": {
				"label": ""
			},
			"speaker": {
				"label": "",
				"name": "",
				"edited": false
			},
			"words": [
				[
					1450,
					1900,
					"추천을"
				],
				[
					1910,
					2220,
					"하는"
				],
				[
					2230,
					2380,
					"게"
				],
				[
					2730,
					2880,
					"뭐"
				],
				[
					3090,
					3300,
					"좋은"
				],
				[
					3370,
					3660,
					"건지"
				],
				[
					3710,
					4240,
					"모르겠어요."
				],
				[
					4630,
					4900,
					"이게."
				]
			],
			"textEdited": "추천을 하는 게 뭐 좋은 건지 모르겠어요. 이게."
		}
	]
"""

"""
call_id	    string  call unique id	uuid4	
t_id	    string	t_id	        미사용	
play_status	string	"멘트 재생 상태* barge in 으로 멘트 중지 'break'"	done | break	break
stt	        string	stt 결과		'추천을 하는 게 뭐 좋은 건지 모르겠어요. 이게.'
dtmf	    string	dtmf		1234
dtmf_status	string	"dtmf 수집 상태* 요청한 자리수까지 수집된 경우 'done'"	done | timeout	done
step	    string	테스트 용도 / 무시하셔도 됩니다.	추가	
stt_detail	string	stt 결과 상세		"[
"""


class TalkRecord(TypedDict):
    call_id: str
    t_id: str
    play_status: str
    stt: str
    stt_detail: str
    dtmf: str
    dtmf_status: str
    step: str


class CallStatus(PyEnum):
    SUCCESS = "success"
    PENDING = "pending"
    INTERRUPTED = "interrupted"
    FAILED = "failed"


class FailureReason(PyEnum):
    ERROR = "error"
    NO_ANSWER = "no_answer"
    DELAYED = "delayed"
    NOT_AVAILABLE = "not_available"
    CALL_TERMINATED = "call_terminated"


class Answer(TableBase):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    answer_list = Column(JSON, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )

    contacts = relationship("Contact", back_populates="answers")
    questions = relationship("Question", back_populates="answers")


class CallLog(TableBase):
    __tablename__ = "call_logs"

    # TODO: API명세와 검증 필요함
    id = Column(String(40), primary_key=True, default=uuid4)
    contact_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    routine_id = Column(Integer, ForeignKey("routines.id"), nullable=False)
    answer_time = Column(TIMESTAMP(timezone=True), nullable=True)
    start_time = Column(TIMESTAMP(timezone=True), nullable=False)
    end_time = Column(TIMESTAMP(timezone=True), nullable=False)
    hangup_disposition = Column(String(10), nullable=True)
    duration = Column(Integer, default=0)
    cause = Column(String(10), nullable=True)
    attempt_count = Column(Integer, default=0)
    status = Column(
        ENUM(CallStatus, name="call_status", create_type=True), nullable=True
    )
    failure_reason = Column(
        ENUM(FailureReason, name="failure_reason", create_type=True), nullable=True
    )

    contacts = relationship("Contact", back_populates="call_logs")
    routines = relationship("Routine", back_populates="call_logs")
