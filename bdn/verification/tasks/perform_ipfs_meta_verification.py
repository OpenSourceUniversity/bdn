import bdn.contract
from bdn.verification.models import Verification
from bdn.certificate.models import Certificate
from bdn.auth.models import User
from django.core.exceptions import ValidationError
from notifications.signals import notify
from celery import shared_task
from bdn.utils.send_email_tasks import verified_certificate_email
from bdn.verification.exceptions import (
    IpfsDataAttributeError, GrantedToUserDoesNotExist,
    VerifierUserDoesNotExist, VerifierUserValidationError,
    VerificationDoesNotExist, VerificationValidationError,
    CertificateDoesNotExist, CertificateValidationError,
    BlockchainVerificationError)


@shared_task
def perform_ipfs_meta_verification(
        verification_ipfs_data, tx_hash,
        block_hash, block_number, meta_ipfs_hash):
    try:
        verifier_id = verification_ipfs_data.get('verifier')
        verification_id = verification_ipfs_data.get('id')
        granted_to_eth = verification_ipfs_data.get(
            'granted_to_eth_address')
    except AttributeError:
        raise IpfsDataAttributeError(
            'verification_ipfs_data AttributeError')
    try:
        granted_to = User.objects.get(username=granted_to_eth)
    except User.DoesNotExist:
        raise GrantedToUserDoesNotExist('GrantedTo DoesNotExist')
    try:
        verifier = User.objects.get(pk=verifier_id)
    except User.DoesNotExist:
        raise VerifierUserDoesNotExist('Verifier DoesNotExist')
    except ValidationError:
        raise VerifierUserValidationError('Verifier ValidationError')
    transaction = bdn.contract.w3.eth.getTransaction(tx_hash)
    from_eth_address = transaction.get('from', '').lower()
    if from_eth_address != verifier.username.lower():
        raise BlockchainVerificationError(
            'Addresses {0} and {1} not equal'.format(
                from_eth_address, verifier.username.lower()))
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
    if granted_to.usersettings.subscribed:
        verified_certificate_email.delay(
            certificate.certificate_title,
            verifier.profile.name_by_profile_type(
                verification.verifier_type),
            granted_to.email
            )
