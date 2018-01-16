import json
import logging
import StringIO

from flask import Blueprint, render_template, send_file

from site_up_checker.default_settings import LOGFILE_PATH
from site_up_checker.validation_config import REQUIREMENTS, SAMPLE_PERIOD


_log = logging.getLogger(__name__)
bp = Blueprint('dashboard', __name__)


@bp.route("/", methods=['GET'])
def index():
    _log.info("Rendering 'index' page")
    website_urls = json.dumps(REQUIREMENTS.keys())

    return render_template(
        'dashboard/index.html',
        urls=website_urls, sample_period=SAMPLE_PERIOD)


@bp.route("/favicon.ico", methods=['GET'])
def favicon():
    return send_file('favicon.ico')


@bp.route("/download_log/", methods=["GET"])
def download_log():
    _log.info("Sending logfile")
    return send_file(LOGFILE_PATH, attachment_filename="website_monitor.log",
                     as_attachment=True)
