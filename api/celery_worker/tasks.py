from celery import Task

from db.database import db_session


class SQLAlchemyTask(Task):
    """
    An abstract Celery Task that ensures that the connection the the
    database is closed on task completion
    """
    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        db_session.remove()
