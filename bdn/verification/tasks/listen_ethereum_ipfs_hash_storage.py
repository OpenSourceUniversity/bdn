import logging
import requests
from django.core.exceptions import ValidationError
from celery import shared_task
from bdn.auth.models import User
from bdn.contract import contract
from bdn.redis import get_redis
from bdn.verification.models import Verification
from bdn.certificate.models import Certificate
from notifications.signals import notify
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
        meta_ipfs_hash = entry_args.get('ipfsHash', b'').decode()
        granted_to_eth = entry_args.get('grantedTo', '')
        if not meta_ipfs_hash or not granted_to_eth:
            logger.error(
                "Event triggered without providing IPFS meta hash or "
                "granted to ETH address")
            continue
        ipfs_link = 'https://ipfs.io/ipfs/' + meta_ipfs_hash
        verification_ipfs_data = requests.get(ipfs_link).json()
        try:
            verifier_id = verification_ipfs_data.get('verifier')
            verification_id = verification_ipfs_data.get('id')
        except AttributeError:
            continue
        try:
            granted_to = User.objects.get(username=granted_to_eth.lower())
            verifier = User.objects.get(pk=verifier_id)
        except User.DoesNotExist:
            continue
        try:
            verification = Verification.objects.get(
                pk=verification_id, verifier=verifier)
        except Verification.DoesNotExist:
            continue
        except ValidationError:
            continue
        if verification.state == 'verified':
            continue
        verification.tx_hash = tx_hash
        verification.block_hash = block_hash
        verification.block_number = block_number
        verification.granted_to = granted_to
        verification.meta_ipfs_hash = meta_ipfs_hash
        verification.move_to_verified()
        verification.save()
        try:
            certificate = Certificate.objects.get(
                id=verification_ipfs_data.get('certificate').get('id'))
        except Certificate.DoesNotExist:
            continue
        notify.send(
            verifier,
            recipient=granted_to,
            verb='verified',
            target=certificate,
            **{
                'actor_active_profile_type': verification.verifier_type,
                'recipient_active_profile_type': verification.granted_to_type
            }
        )

        if block_number > last_block:
            redis_db.set('_verification_filter_block', block_number)

        perform_ipfs_meta_verification.delay()
