import os
from celery import Celery


BROKER_URL = os.environ.get("CELERY_BROKER_URL")
BACKEND_URL = os.environ.get("CELERY_RESULT_BACKEND")

app = Celery(
    'celery_worker',
    backend=BACKEND_URL,
    broker=BROKER_URL,
    include=['celery_worker.tasks']
)

if __name__ == '__main__':
    app.start()
