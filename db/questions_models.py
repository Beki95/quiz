from datetime import datetime as dt

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from core.base_db import Base


class Quiz(Base):
    __tablename__ = 'quiz'

    id = Column(Integer, primary_key=True, index=True)
    questions = relationship('Question', back_populates='quiz', lazy='joined')

    created_at = Column(DateTime, default=dt.utcnow)


quiz = Quiz.__tablename__


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text)
    answer = Column(String(length=255))

    created_at = Column(DateTime, default=dt.utcnow)
    question_created_at = Column(DateTime)

    quiz_id = Column(Integer, ForeignKey("quiz.id"))
    quiz = relationship('Quiz', back_populates='questions', lazy='joined')


question = Question.__tablename__
