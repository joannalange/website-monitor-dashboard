from site_up_checker.app_factory import create_celery_app, create_app


app = create_app()
celery = create_celery_app(app)
