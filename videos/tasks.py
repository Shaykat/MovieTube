from celery.task import task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@task(name="compress_video")
def compress_video(input_path, output_path):
    """sends an email when feedback form is filled successfully"""
    logger.info("Sent feedback email")