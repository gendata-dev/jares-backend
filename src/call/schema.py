from sqlalchemy import Column, Integer, ForeignKey, JSON, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from typing_extensions import TypedDict

from schema import Base

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
    play_status: str  # done or break
    stt: str
    stt_detail: str
    dtmf: str
    dtmf_status: str
    step: str


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("contacts.id"), nullable=False)
    survey_id = Column(Integer, ForeignKey("surveys.id"), nullable=False)
    answer_list = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    user = relationship("Contact", back_populates="answers")
    survey = relationship("Survey", back_populates="answers")
    question = relationship("Question", back_populates="answers")
