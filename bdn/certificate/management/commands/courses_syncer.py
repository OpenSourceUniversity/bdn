import asyncio
import json
import web3
import time
from web3.auto import w3
from django.core.management.base import BaseCommand, CommandError
from bdn.certificate.models import Certificate


CERTIFICATE_STORAGE_JSON = '/home/jordan/Projects/platform/build/contracts/CertificateStorage.json'


class Command(BaseCommand):
    help = 'Syncs courses through web3'

    def __init__(self, *args, **kwargs):
        self.w3 = web3.Web3(web3.HTTPProvider('http://127.0.0.1:8545'))
        return super().__init__()

    @property
    def contractInstance(self):
        contract_interface = json.load(open(CERTIFICATE_STORAGE_JSON))
        for _, network in contract_interface['networks'].items():
            return self.w3.eth.contract(
                address=network['address'],
                abi=contract_interface['abi'])

    def handle_event(self, event):
        print(event)

    async def log_loop(self, event_filter, poll_interval):
        event_filter.get_all_entries()
        while True:
            for event in event_filter.get_new_entries():
                self.handle_event(event)
            await asyncio.sleep(poll_interval)

    def handle(self, *args, **options):
        certificate_created_filter = self.contractInstance.eventFilter(
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
