import asyncio
import time
from datetime import datetime
from eth_utils import force_text
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import make_aware
from bdn.certificate.models import Certificate
from bdn.contract import contract


class Command(BaseCommand):
    help = 'Syncs courses through web3'

    def handle(self, *args, **options):
        contract_instance = contract('CertificateStorage')
        certificate_created_filter = contract_instance.eventFilter(
            'CertificateCreated',
            {
                'fromBlock': 0,
                'toBlock': 'latest',
            })
        loop = asyncio.get_event_loop()
        try:
            task = loop.create_task(
                self.log_loop(certificate_created_filter, 0.5))
            loop.run_until_complete(task)
        finally:
            loop.close()

    async def log_loop(self, event_filter, poll_interval):
        event_filter.get_all_entries()
        while True:
            for event in event_filter.get_new_entries():
                print(event)
                self.handle_event(event)
            await asyncio.sleep(poll_interval)

    def handle_event(self, event):
        if event['event'] == 'CertificateCreated':
            self.certificate_created(event)

    def certificate_created(self, event):
        index = event['args']['index']
        fns = contract('CertificateStorage').functions
        addresses = fns.getCertificateAddressesByIndex(index).call()
        certificate_data = fns.getCertificateDataByIndex(index).call()

        academy, course, learner, creator = addresses
        name, subject, verified, score, expiration_date = certificate_data

        name = force_text(name[0].rstrip(b'\0')) + force_text(name[1].rstrip(b'\0'))
        subject = force_text(subject[0].rstrip(b'\0')) + force_text(subject[1].rstrip(b'\0'))
        expiration_date = datetime.utcfromtimestamp(expiration_date)

        certificate = Certificate(
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
