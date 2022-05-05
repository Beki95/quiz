from celery import Celery

from decouple import config

celery_app = celery = Celery(__name__)
celery.conf.broker_url = config('CELERY_BROKER_URL')
celery.conf.timezone = 'Asia/Bishkek'
