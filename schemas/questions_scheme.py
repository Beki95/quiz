import datetime
from datetime import datetime as dt

from pydantic import BaseModel


class QuestionCount(BaseModel):
    questions_num: int


class QuestionScheme(BaseModel):
    id: int
    question: str
    answer: str
    created_at: datetime.datetime = dt.utcnow()
    question_created_at: datetime.datetime = dt.utcnow()


class QuizScheme(BaseModel):
    id: int
    created_at: datetime.datetime
    questions: list[QuestionScheme, ...]
