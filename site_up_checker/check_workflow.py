import logging
from celery import chain, group

from site_up_checker.validation_config import REQUIREMENTS

_log = logging.getLogger(__name__)


class CheckWorkflow(object):
    def __call__(self):
        from tasks import check_content, get_website_content, process_results

        tasks = []
        # iterate over all websites - for each of them create a tasks chord,
        # where first task will get the website's content and the second task
        # will analyze it
        _log.info("Creating workflow")

        for url_i, requirements_i in REQUIREMENTS.iteritems():
            # requirements for the website content, e.g. it must contain a
            # certain string

            single_website_tasks = chain(
                get_website_content.s(url_i),
                check_content.s(requirements_i, url_i)
            )

            tasks.append(single_website_tasks)

        # create a tasks group so that checks are ran simultaneously
        workflow = chain(group(tasks), process_results.s())

        # run job
        job = workflow()
        _log.info("Job submitted")
        return job.id
