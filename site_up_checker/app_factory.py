import logging

from celery import Celery
from flask import Flask


_log = logging.getLogger(__name__)


def create_app():
    _log.info("Creating app")

    app = Flask(__name__, static_folder='frontend/static',
                template_folder='frontend/templates')
    app.config.from_object('site_up_checker.default_settings')
    app.config.from_envvar('SITE_UP_CHECKER_SETTINGS')

    # Configure logging.
    from site_up_checker import _log as root_logger

    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root_logger.addHandler(ch)
    root_logger.setLevel(logging.INFO)
    # otherwise you get double logging
    root_logger.propagate = False

    # Register blueprints
    from site_up_checker.frontend.api.endpoints import bp as api_bp
    from site_up_checker.frontend.dashboard.views import bp as dashboard_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(dashboard_bp)

    return app


def create_celery_app(app):
    _log.info("Creating celery app")

    app = app or create_app()

    celery = Celery(__name__, backend='amqp',
                    broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)

    import site_up_checker.tasks

    return celery
