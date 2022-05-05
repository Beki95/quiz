from .worker import celery_app
from .tasks import task_get_questions

__all__ = [celery_app]
