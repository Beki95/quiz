from pydantic import parse_obj_as

from core import celery_app
from core.base_db import get_context_db
from core.service import (
    RequestForQuestions, GettingUniqueData, GetUniqueValues, QuestionListCreate
)
from repositories.quiz import QuizRepository
from schemas.questions_scheme import QuestionScheme


@celery_app.task(bind=True)
def task_get_questions(self, count):
    with get_context_db() as db:
        quiz_id = QuizRepository(db=db).create()
        questions = QuestionListCreate(db=db)
        ids = questions.list()
        requester = RequestForQuestions()
        checker = GetUniqueValues()
        data = GettingUniqueData(
            checker=checker,
            requester=requester
        ).send(count=count, ids_values=ids)
        data = parse_obj_as(list[QuestionScheme], data)
        questions.create(data=data, quiz_id=quiz_id)
    return quiz_id
