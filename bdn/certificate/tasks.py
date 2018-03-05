import logging
from celery import shared_task
from web3 import Web3
from datetime import datetime
from django.utils.timezone import make_aware
from bdn.certificate.models import Certificate
from bdn.contract import contract


logger = logging.getLogger(__name__)


@shared_task
def create_certificate(index):
    fns = contract('CertificateStorage').functions
    addresses = fns.getCertificateAddressesByIndex(index).call()
    certificate_data = fns.getCertificateDataByIndex(index).call()

    academy, course, learner, creator = addresses
    uid, name, subject, verified, score, expiration_date = certificate_data

    def normalize(s): return Web3.toText(s.rstrip(b'\0'))
    name = normalize(name[0]) + normalize(name[1])
    subject = normalize(subject[0]) + normalize(subject[1])
    expiration_date = datetime.utcfromtimestamp(expiration_date)

    certificate = Certificate(
        uid=uid,
        index=index,
        academy=academy,
        course=course,
        learner=learner,
        name=name,
        subject=subject,
        verified=verified,
        score=score,
        creator=creator,
        expiration_date=make_aware(expiration_date)
    )
    certificate.save()

    logger.info('Created certificate with index {0}'.format(index))
