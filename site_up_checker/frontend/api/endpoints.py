import logging

from flask import Blueprint
from flask.json import jsonify

from site_up_checker.check_workflow import CheckWorkflow


_log = logging.getLogger(__name__)

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
