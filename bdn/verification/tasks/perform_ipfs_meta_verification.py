import logging
from celery import shared_task


logger = logging.getLogger(__name__)


@shared_task
def perform_ipfs_meta_verification():
    pass
