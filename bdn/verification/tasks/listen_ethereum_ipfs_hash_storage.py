import logging
from celery import shared_task
from bdn.auth.models import User
from bdn.contract import contract
from bdn.redis import get_redis
from bdn.verification.models import Verification
from .perform_ipfs_meta_verification import perform_ipfs_meta_verification


logger = logging.getLogger(__name__)


@shared_task
def listen_ethereum_ipfs_hash_storage():
    redis_db = get_redis()
    verification_storage = contract('VerificationStorage')
    event = verification_storage.events.Verification

    last_block = redis_db.get('_verification_filter_block') or 0
    if last_block != 0:
        last_block = int(last_block)

    hash_filter = event.createFilter(fromBlock=last_block)

    for entry in hash_filter.get_all_entries():
        tx_hash = entry['transactionHash'].hex()
        block_hash = entry['blockHash'].hex()
        block_number = int(entry['blockNumber'])
        entry_args = entry['args']
        meta_ipfs_hash = entry_args.get('meta_ipfs_hash', b'').decode()
        granted_to_eth = entry_args.get('granted_to', '')
        if not meta_ipfs_hash or not granted_to_eth:
            continue

        try:
            granted_to = User.objects.get(username=granted_to_eth.lower())
        except User.DoesNotExist:
            granted_to = None

        verification, _ = Verification.objects.get_or_create(
            tx_hash=tx_hash,
            block_hash=block_hash,
            block_number=block_number,
            granted_to=granted_to,
            meta_ipfs_hash=meta_ipfs_hash)

        if block_number > last_block:
            redis_db.set('_verification_filter_block', block_number)

        perform_ipfs_meta_verification.delay()
