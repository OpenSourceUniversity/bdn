import asyncio
import json
import web3
import time
from datetime import datetime
from eth_utils import force_text
from web3.auto import w3
from django.core.management.base import BaseCommand, CommandError
from django.utils.timezone import make_aware
from bdn.certificate.models import Certificate


CERTIFICATE_STORAGE_JSON = '/home/jordan/Projects/platform/build/contracts/CertificateStorage.json'


class Command(BaseCommand):
    help = 'Syncs courses through web3'

    def __init__(self, *args, **kwargs):
        self.w3 = web3.Web3(web3.HTTPProvider('http://127.0.0.1:8545'))
        return super().__init__()

    def handle(self, *args, **options):
        certificate_created_filter = self.contract_instance.eventFilter(
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

    @property
    def contract_instance(self):
        contract_interface = json.load(open(CERTIFICATE_STORAGE_JSON))
        for _, network in contract_interface['networks'].items():
            return self.w3.eth.contract(
                address=network['address'],
                abi=contract_interface['abi'])

    async def log_loop(self, event_filter, poll_interval):
        event_filter.get_all_entries()
        while True:
            for event in event_filter.get_new_entries():
                self.handle_event(event)
            await asyncio.sleep(poll_interval)

    def handle_event(self, event):
        if event['event'] == 'CertificateCreated':
            self.certificate_created(event)

    def certificate_created(self, event):
        index = event['args']['index']
        fns = self.contract_instance.functions
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
