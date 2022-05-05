from datetime import datetime as dt

from db.questions_models import Quiz
from repositories.base import BaseRepository


class QuizRepository(BaseRepository):

    async def get(self):
        return self.db.query(Quiz).order_by(Quiz.id.desc()).first()

    def create(self):
        obj = Quiz(created_at=dt.utcnow())
        self.db.add(obj)
        self.db.commit()
        return obj.id
