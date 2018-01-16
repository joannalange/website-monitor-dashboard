import logging

from flask import Blueprint, send_file
from flask.json import jsonify

from site_up_checker.check_workflow import CheckWorkflow
from site_up_checker.default_settings import LOGFILE_PATH


_log = logging.getLogger(__name__)
# setup file logger
_file_log = logging.getLogger(__name__ + ".filelogger")
file_handler = logging.FileHandler("/var/log/website_monitor.log")
_file_log.addHandler(file_handler)

bp = Blueprint('siteup', __name__, url_prefix='/api')


@bp.route('/status/<job_id>/', methods=['GET'])
def get_status(job_id):
    """
    Get the job's status

    :param job_id: job identifier
    :return: status of the job
    """
    from site_up_checker.application import celery

    result = celery.AsyncResult(job_id)
    response = {'status': result.status}
    _log.info("Status of job %s: %s", job_id, result.status)
    return jsonify(response)


@bp.route('/result/<job_id>/', methods=['GET'])
def get_result(job_id):
    """
    Get the result of a previous job submission.

    :param job_id: job identifier
    :return: job's result in json format
    """
    _log.info("Getting results for job_id %s", job_id)

    from site_up_checker.tasks import process_results

    result = process_results.AsyncResult(job_id).get()

    log_results(result)

    response = {'result': result}
    return jsonify(response)


@bp.route('/run_checks/', methods=['GET'])
def run_checks():
    """
    :return: The job id
    """
    workflow = CheckWorkflow()
    job_id = workflow()
    _log.info("Running checks, job_id: %s", job_id)
    return jsonify({'id': job_id}), 202


def log_results(final_results):
    """
    Log results to file
    """
    _file_log.info("Check performed: %s", final_results["last_checked"])

    # iterate through websites and log the check results
    for url, website_data in final_results["websites"].iteritems():
        up_or_down = "UP" if website_data["is_up"] else "DOWN"
        log_msg = "url: {}; status: {};".format(url, up_or_down)

        if website_data["is_up"]:
            # if up log if content correct and the response time
            log_msg += " correct content: {}; response time: {};".format(
                website_data["content_ok"], website_data["response_time"])
        else:
            # if down log the error
            log_msg += " error: {}".format(website_data["reason"])

        _file_log.info(log_msg)
