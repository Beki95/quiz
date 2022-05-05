import asyncio
from abc import ABC, abstractmethod

import aiohttp
from decouple import config
# interface
from sqlalchemy.orm import Session

from repositories.questions import QuestionRepository


class Request(ABC):

    @abstractmethod
    def __init__(self, url: str):
        ...

    @abstractmethod
    async def request(self, count: int):
        ...

    @abstractmethod
    def response(self, count):
        ...


class RequestForQuestions(Request):

    def __init__(self, url: str = config('API_URL')) -> None:
        self.api_url = url

    async def request(self, count: int) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    self.api_url, params={'count': count}
            ) as res:
                return await res.json()

    async def response(self, count: int) -> dict:
        data = await self.request(count)
        return data


def get_api_response(count: int, requester: Request) -> list:
    loop = asyncio.get_event_loop()
    data = loop.run_until_complete(requester.response(count))
    return data


# interface
class Checker(ABC):

    @abstractmethod
    def __init__(self) -> None:
        ...

    @abstractmethod
    def check_values_for_uniq(self, api_values: list[dict, ...],
                              ids_values: list[int, ...]):
        ...


class GetUniqueValues(Checker):
    __slots__ = ['ids_values', 'uniq']

    def __init__(self) -> None:
        self.ids_values = []

    def check_values_for_uniq(self, api_values: list[dict, ...],
                              ids_values: list):
        uniq = []
        self.ids_values.extend(ids_values)
        for i in range(len(api_values)):
            _id = api_values[i]['id']
            if _id not in self.ids_values:
                uniq.append(api_values[i])
        return uniq


class GettingUniqueData:

    def __init__(self, checker: Checker, requester: Request):
        self.checker = checker
        self.requester = requester
        self.uniq = []

    @classmethod
    def get_ids(cls, list_: list[dict, ...]) -> list[int, ...]:
        list_ = [_['id'] for _ in list_]
        return list_

    def send(self, count, ids_values):
        data = get_api_response(count, self.requester)
        uniq = self.checker.check_values_for_uniq(data, ids_values)
        self.uniq.extend(uniq)
        if len(uniq) != count:
            count -= len(uniq)
            ids = self.get_ids(uniq)  # getting the id of the new data
            return self.send(count, ids)
        return self.uniq


class QuestionListCreate:

    def __init__(self, db: Session):
        self.db = db

    def list(self) -> list[int, ...]:
        return QuestionRepository(db=self.db).get_all()

    def create(self, data: list, quiz_id: int) -> None:
        QuestionRepository(db=self.db).create(questions=data, quiz_id=quiz_id)
