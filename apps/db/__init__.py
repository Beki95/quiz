from .base import engine, Base
from .questions_models import quiz, question

Base.metadata.create_all(bind=engine)

