# flake8: noqa
from unittest.mock import MagicMock, patch
from django.test import TestCase
from bdn.certificate.models import Certificate
from bdn.auth.models import User
from .models import Verification
from .tasks import (
    listen_ethereum_ipfs_hash_storage, perform_ipfs_meta_verification)


class fake_get_redis:
    def get(self, key_name):
        return 1

    def __call__(self):
        return self.__class__()


class fake_hash_storage_contract:
    def __init__(self, events):
        self.events = events

    def __call__(self, contract_name):
        instance = type('', (), {})
        filter_mock = MagicMock()
        filter_mock.get_all_entries.return_value = self.events
        instance.events = MagicMock()
        instance.events.Verification.createFilter.return_value = filter_mock
        return instance


class fake_ipfs_request_get:
    def __init__(self, ipfs_verification_results):
        self.ipfs_verification_results = ipfs_verification_results
        self.exec_count = 0

    def __call__(self, *args):
        instance = type('', (), {})
        instance = MagicMock()
        instance.json.return_value = self.ipfs_verification_results[
            self.exec_count
        ]
        self.exec_count += 1
        return instance


class VerificationTests(TestCase):
    def setUp(self):
        self.verifier, _ = User.objects.get_or_create(username='0x01')
        self.certificate = Certificate(
            academy_title='test',
            academy_link='http://test.com/',
            course_title='test',
            learner_eth_address='0x0',
        )
        self.certificate.save()
        self.verification = Verification(
            certificate=self.certificate, verifier=self.verifier)
        self.verification.save()

    @patch('bdn.redis.get_redis', fake_get_redis())
    @patch('bdn.contract.contract', fake_hash_storage_contract([
        {
            'transactionHash': 1.0,
            'blockHash': 1.0,
            'blockNumber': '1',
            'args': {
                'ipfsHash': bytes('some_ipfs_hash', 'utf-8'),
                'grantedTo': 'granted_to',
            }
        }
    ]))
    @patch('requests.get', fake_ipfs_request_get([
        {
            'a': 1
        }
    ]))
    def test_verification_task(self):
        # with patch('celeryconfig.CELERY_ALWAYS_EAGER', True, create=True):
        listen_ethereum_ipfs_hash_storage()

    def tearDown(self):
        self.verification.delete()
        self.certificate.delete()
        self.verifier.delete()
