import logging

from flask.json import jsonify
from flask import Blueprint, render_template


_log = logging.getLogger(__name__)
bp = Blueprint('dashboard', __name__)


@bp.route("/", methods=['GET'])
def index():
    _log.info("Rendering 'index' page")

    return render_template('dashboard/index.html')
