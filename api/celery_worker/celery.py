import os
from celery import Celery
from celery.schedules import crontab


BROKER_URL = os.environ.get("CELERY_BROKER_URL")
BACKEND_URL = os.environ.get("CELERY_RESULT_BACKEND")

app = Celery(
    'celery_worker',
    backend=BACKEND_URL,
    broker=BROKER_URL,
    include=['celery_worker.tasks']
)

app.conf.beat_schedule = {
    "setup_musicians": {
        "task": "get_links",
        "schedule": crontab(hour=0, minute=0, day_of_week='sunday')
    },
    "setup_songs": {
        "task": "get_houses_info",
        "schedule": crontab(hour=0, minute=0, day_of_week='sunday')
    },
    "setup_ranking": {
        "task": "get_flats_info",
        "schedule": crontab(hour=0, minute=0, day_of_week='sunday')
    },
}

if __name__ == '__main__':
    app.start()
