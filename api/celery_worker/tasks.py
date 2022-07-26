import logging

from celery import Task

from .celery import app
from .tasks_helpers_otodom import scrap_houses_info_otodom, scrap_flats_info_otodom
from .tasks_helpers_olx import scrap_houses_info_olx, scrap_flats_info_olx
from .task_helpers_scrap_links import scrap_links
from db.database import db_session

logging.getLogger(__name__)


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
    logging.info("DB filled with new links.")


@app.task(name="get_houses_info", base=SQLAlchemyTask)
def get_houses_info():
    scrap_houses_info_otodom(db_session)
    scrap_houses_info_olx(db_session)
    logging.info("Houses filled with info.")


@app.task(name="get_flats_info", base=SQLAlchemyTask)
def get_flats_info():
    scrap_flats_info_otodom(db_session)
    scrap_flats_info_olx(db_session)
    logging.info("Flats filled with info.")
