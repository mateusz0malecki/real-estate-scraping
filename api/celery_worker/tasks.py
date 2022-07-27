from celery import Task

from .celery import app
from .tasks_helpers import scrap_links, scrap_houses_info, scrap_flats_info
from db.database import db_session


class SQLAlchemyTask(Task):
    """
    An abstract Celery Task that ensures that the connection the the
    database is closed on task completion
    """
    abstract = True

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        db_session.remove()


@app.task(name="get_links", base=SQLAlchemyTask)
def get_links():
    estates = ['dom', 'mieszkanie']
    for_sale_conditions = [True, False]
    cities = [
        'gdansk',
        'szczecin',
        'bialystok',
        'torun',
        'bydgoszcz',
        'olsztyn',
        'warszawa',
        'lublin',
        'rzeszow',
        'krakow',
        'katowice',
        'opole',
        'wroclaw',
        'lodz',
        'poznan',
        'zielona-gora',
        'gorzow-wielkopolski',
        'kielce'
    ]
    for estate in estates:
        for for_sale in for_sale_conditions:
            for city in cities:
                scrap_links(db_session, estate, for_sale, city)
    print("DB filled with new links.")


@app.task(name="get_houses_info", base=SQLAlchemyTask)
def get_houses_info():
    scrap_houses_info(db_session)
    print("Houses filled with info.")


@app.task(name="get_flats_info", base=SQLAlchemyTask)
def get_flats_info():
    scrap_flats_info(db_session)
    print("Flats filled with info.")
