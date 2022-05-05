from db.questions_models import Question
from repositories.base import BaseRepository
from schemas.questions_scheme import QuestionScheme


class QuestionRepository(BaseRepository):

    def get_all(self):
        ids = [x.id for x in self.db.query(Question.id)]
        return ids

    def create(self, questions: list[QuestionScheme], quiz_id: int) -> None:
        objs = [Question(**i.dict(), quiz_id=quiz_id) for i in questions]
        self.db.add_all(objs)
        self.db.commit()
