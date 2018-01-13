import json
import logging

from flask import Blueprint, render_template

from site_up_checker.validation_config import REQUIREMENTS, SAMPLE_PERIOD


_log = logging.getLogger(__name__)
bp = Blueprint('dashboard', __name__)


@bp.route("/", methods=['GET'])
def index():
    _log.info("Rendering 'index' page")
    website_urls = json.dumps(REQUIREMENTS.keys())

    return render_template('dashboard/index.html',
                           urls=website_urls, sample_period=SAMPLE_PERIOD)
