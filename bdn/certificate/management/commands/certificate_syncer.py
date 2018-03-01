import asyncio
import logging
from django.core.management.base import BaseCommand
from bdn.contract import contract
from bdn.certificate.tasks import create_certificate


logger = logging.getLogger(__name__)


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
                self.handle_event(event)
            await asyncio.sleep(poll_interval)

    def handle_event(self, event):
        logger.info('{0} event received'.format(event['event']))
        if event['event'] == 'CertificateCreated':
            self.certificate_created(event)

    def certificate_created(self, event):
        index = event['args']['index']
        create_certificate.delay(index)
