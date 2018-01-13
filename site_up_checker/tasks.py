import logging
import requests

from celery import current_app as celery_app

import page_validator

_log = logging.getLogger(__name__)


@celery_app.task
def get_website_content(url):
    """
    Makes a request to the given url and returns a dictionary with
    information about the response
    :param url:
    :return: dictionary:
        {
            "status": status code of the response,
            "html_content": content of the website (if status other than 200 it's empty)
            "reason": message (error or 'reason') when a request doesn't succeed
        }
    """
    response_info = {"status": None, "html_content": "", "reason": "", "response_time": None}

    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError as e:
        # url not found
        response_info["reason"] = e.message
    else:
        if response.status_code != 200:
            response_info["reason"] = response.reason
        else:
            response_info["html_content"] = response.text

        response_info["status"] = response.status_code
        response_info["response_time"] = response.elapsed.total_seconds()
    _log.info("task get content result: %s", response_info)
    return response_info


@celery_app.task
def check_content(response_info, requirements, url):
    """
    If the status code of the response was 200 checks if the
    website's content meets the given requierements
    """
    _log.info("Checking content of: %s", url)
    content_ok = False
    if response_info["status"] == 200:
        # we could do a simple substring check on the html content
        # but then we would be looking also in the document's comments,
        # scripts and css - we only want the strings mentioned in
        # requierements to be present in the raw text
        content_ok = page_validator.check_page(
                response_info["html_content"], requirements)

    result = {
        "url": url,
        "is_up": response_info["status"] == 200,
        "content_ok": content_ok,
        "reason": response_info["reason"]
    }

    return result


@celery_app.task
def process_results(results):
    """
    Combines results from multiple websites

    :param results: a list of results (dictionaries) from multiple check_content tasks
    :return: dictionary:
        {
            "url1": check_result dict,
            ...
        }
    """
    _log.info("Processing results")
    final_results = {}

    for website in results:
        final_results[website["url"]] = website

    return final_results
