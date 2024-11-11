from abc import ABCMeta, abstractmethod

from call.schema import TalkRecord


repo_dict = dict()


class CallRepository:
    """Interface"""

    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def repository(self):
        raise NotImplementedError

    @abstractmethod
    async def save(self, talk_record: TalkRecord) -> TalkRecord:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, talk_recordv: TalkRecord) -> TalkRecord:
        raise NotImplementedError


class CallDictRepository(CallRepository):
    def __init__(self):
        self._repository = repo_dict

    @property
    def repository(self):
        return self._repository

    async def save(self, talk_record: TalkRecord) -> TalkRecord:
        self.repository[talk_record.get("id")] = talk_record
        return talk_record

    async def delete(self, talk_record: TalkRecord) -> TalkRecord:
        del self.repository[talk_record.get("id")]
        return talk_record
