import logging
import requests
import json
from celery import shared_task
from .perform_ipfs_meta_verification import perform_ipfs_meta_verification
from bdn.verification.exceptions import (
    NoArgumentsError, JsonDecodeError)


IPFS_HOST = 'https://ipfs.io/ipfs/'

logger = logging.getLogger(__name__)


@shared_task
def perform_ipfs_meta_verifications_array(entry):
    tx_hash = entry['transactionHash']
    block_hash = entry['blockHash']
    block_number = int(entry['blockNumber'])
    entry_args = entry['args']
    meta_ipfs_hash = entry_args.get('ipfsHash', '')
    if not meta_ipfs_hash:
        raise NoArgumentsError(
            'Event triggered without providing IPFS meta hash')
    ipfs_link = IPFS_HOST + meta_ipfs_hash
    try:
        verification_ipfs_data_arr = requests.get(ipfs_link).json()
    except json.decoder.JSONDecodeError:
        raise JsonDecodeError('Can not decode IPFS data')
    if not isinstance(verification_ipfs_data_arr, list):
        verification_ipfs_data_arr = [verification_ipfs_data_arr]
    for verification_ipfs_data in verification_ipfs_data_arr:
        perform_ipfs_meta_verification.delay(
            verification_ipfs_data, tx_hash,
            block_hash, block_number, meta_ipfs_hash)
