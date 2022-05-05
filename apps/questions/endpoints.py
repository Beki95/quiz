from fastapi import APIRouter
from fastapi import Depends

from core.base_db import get_db
from core.tasks import task_get_questions
from repositories.quiz import QuizRepository
from schemas.questions_scheme import QuestionCount

router = APIRouter()


@router.post("/")
async def create_questions(count: QuestionCount, db=Depends(get_db)):
    count = count.dict().get('questions_num')
    data = await QuizRepository(db=db).get()
    task_get_questions.delay(count)
    return data
