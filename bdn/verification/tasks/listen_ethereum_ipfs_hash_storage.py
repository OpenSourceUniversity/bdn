import logging
import json
from celery import shared_task
from bdn import contract
from bdn import redis
from .perform_ipfs_meta_verification import perform_ipfs_meta_verification


logger = logging.getLogger(__name__)


@shared_task
def listen_ethereum_ipfs_hash_storage():
    redis_db = redis.get_redis()
    verification_storage = contract.contract('VerificationStorage')
    event = verification_storage.events.Verification

    last_block = redis_db.get('_verification_filter_block') or 0
    if last_block != 0:
        last_block = int(last_block)

    hash_filter = event.createFilter(fromBlock=last_block)

    for entry in hash_filter.get_all_entries():
        block_number = int(entry['blockNumber'])
        entry_args = dict(entry['args'])
        entry_data = {
            'transactionHash': entry['transactionHash'].hex(),
            'blockHash': entry['blockHash'].hex(),
            'blockNumber': entry['blockNumber'],
            'args': {
                'ipfsHash': entry_args.get('ipfsHash', b'').decode(),
                'grantedTo': entry_args.get('grantedTo', ''),
            },
        }
        perform_ipfs_meta_verification.delay(entry_data)
        if block_number > last_block:
            redis_db.set('_verification_filter_block', block_number)
