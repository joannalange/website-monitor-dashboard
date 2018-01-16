from kombu import Exchange, Queue


# Celery settings
CELERY_BROKER_URL = 'amqp://guest@siteupchecker_rabbitmq_1'
CELERY_DEFAULT_QUEUE = 'site_up_checker'
CELERY_QUEUES = (
    Queue('site_up_checker', Exchange('site_up_checker'), routing_key='site_up_checker'),
)
CELERY_RESULT_BACKEND = 'redis://siteupchecker_redis_1/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYD_CONCURRENCY = 8
CELERYD_NODES = 3

LOGFILE_PATH = "/var/log/website_monitor.log"
