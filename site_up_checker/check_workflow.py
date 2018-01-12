import logging
from celery import chain, group

_log = logging.getLogger(__name__)


class CheckWorkflow(object):
    def __init__(self, settings):
        self.settings = settings

    def __call__(self):
        from tasks import check_content, get_website_content, process_results

        tasks = []
        # iterate over all websites - for each of them create a tasks chord,
        # where first task will get the website's content and the second task
        # will analyze it
        _log.info("Creating workflow")

        for website_data in self.settings["websites"]:
            url = website_data["url"]
            # requirements for the website content, e.g. it must contain a
            # certain string
            requirements = website_data["requirements"]

            single_website_tasks = chain(
                get_website_content.s(url),
                check_content.s()
            )

            tasks.append(single_website_tasks)

        # create a tasks group so that checks are ran simultaneously
        workflow = chain(group(tasks), process_results.s())

        # run job
        job = workflow()
        _log.info("Job submitted")
        return job.id
