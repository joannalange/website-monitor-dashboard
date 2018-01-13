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
        response = requests.get(url, timeout=3)
    except BaseException as e:
        # request raised an error
        response_info["reason"] = str(e.message)
    else:
        if response.status_code != 200:
            response_info["reason"] = str(response.reason)
        else:
            response_info["html_content"] = response.text

        response_info["status"] = response.status_code

        response_time = response.elapsed.total_seconds()
        if isinstance(response_time, float):
            # round it to 4th decimal
            response_info["response_time"] = ("%.4f" % response_time)
    _log.info("returning: #%s#", response_info)
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
        "reason": response_info["reason"],
        "response_time": response_info["response_time"]
    }

    return result


@celery_app.task
def process_results(results, last_checked):
    """
    Combines results from multiple websites

    :param results: a list of results (dictionaries) from multiple check_content tasks
    :param last_checked: date and time of when the last (this) check was ran
    :return: dictionary:
        {
            "url1": check_result dict,
            ...
        }
    """
    _log.info("Processing results")

    final_results = {"websites": {}, "last_checked": last_checked}

    for website in results:
        final_results["websites"][website["url"]] = website

    return final_results
