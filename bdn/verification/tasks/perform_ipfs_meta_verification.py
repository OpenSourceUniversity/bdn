import logging
import requests
from bdn.verification.models import Verification
from bdn.certificate.models import Certificate
from bdn.auth.models import User
from django.core.exceptions import ValidationError
from notifications.signals import notify
from celery import shared_task
from bdn.verification.exceptions import (
    NoArgumentsError, IpfsDataAttributeError,
    GrantedToUserDoesNotExist, VerifierUserDoesNotExist,
    VerifierUserValidationError, VerificationDoesNotExist,
    VerificationValidationError, CertificateDoesNotExist,
    CertificateValidationError)


IPFS_HOST = 'https://ipfs.io/ipfs/'

logger = logging.getLogger(__name__)


@shared_task
def perform_ipfs_meta_verification(entry):
    tx_hash = entry['transactionHash']
    block_hash = entry['blockHash']
    block_number = int(entry['blockNumber'])
    entry_args = entry['args']
    meta_ipfs_hash = entry_args.get('ipfsHash', '')
    granted_to_eth = entry_args.get('grantedTo', '')
    if not meta_ipfs_hash or not granted_to_eth:
        raise NoArgumentsError(
            "Event triggered without providing IPFS meta hash or "
            "granted to ETH address")
    ipfs_link = IPFS_HOST + meta_ipfs_hash
    verification_ipfs_data = requests.get(ipfs_link).json()
    try:
        verifier_id = verification_ipfs_data.get('verifier')
        verification_id = verification_ipfs_data.get('id')
    except AttributeError:
        raise IpfsDataAttributeError('verification_ipfs_data AttributeError')
    try:
        granted_to = User.objects.get(username=granted_to_eth.lower())
    except User.DoesNotExist:
        raise GrantedToUserDoesNotExist('GrantedTo DoesNotExist')
    try:
        verifier = User.objects.get(pk=verifier_id)
    except User.DoesNotExist:
        raise VerifierUserDoesNotExist('Verifier DoesNotExist')
    except ValidationError:
        raise VerifierUserValidationError('Verifier ValidationError')
    try:
        verification = Verification.objects.get(
            pk=verification_id, verifier=verifier)
    except Verification.DoesNotExist:
        raise VerificationDoesNotExist('Verification DoesNotExist')
    except ValidationError:
        raise VerificationValidationError('Verification ValidationError')
    if verification.state == 'verified':
        return
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
        raise CertificateDoesNotExist('Certificate DoesNotExist')
    except ValidationError:
        raise CertificateValidationError('Certificate ValidationError')
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
