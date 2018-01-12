import logging
from celery import current_app as celery_app

_log = logging.getLogger(__name__)


@celery_app.task
def get_website_content(url):
    return "some content"


@celery_app.task
def check_content(url):
    return True


@celery_app.task
def process_results(results):
    _log.info("processing results")

    res = {
        "website1": "site-up",
        "website2": "site-down",
        "website3": "site-incorrect"
    }
    return res
