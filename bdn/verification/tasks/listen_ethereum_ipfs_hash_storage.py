import logging
from celery import shared_task


logger = logging.getLogger(__name__)


@shared_task
def listen_ethereum_ipfs_hash_storage():
    print("baba 4")
    return 1
