# flake8: noqa
import uuid
from unittest.mock import MagicMock, patch
from django.test import TestCase
from bdn.certificate.models import Certificate
from bdn.auth.models import User
from bdn.celery import app as celeryapp
from .models import Verification
from .tasks import (
    listen_ethereum_ipfs_hash_storage, perform_ipfs_meta_verification)
from bdn.verification.exceptions import (
    NoArgumentsError, IpfsDataAttributeError,
    GrantedToUserDoesNotExist, VerifierUserDoesNotExist,
    VerifierUserValidationError, VerificationDoesNotExist,
    VerificationValidationError, CertificateDoesNotExist,
    CertificateValidationError)


class fake_get_redis:
    def __init__(self, get_result):
        self._get_result = get_result

    def __call__(self):
        mock = MagicMock()
        mock.get.return_value = self._get_result
        return mock


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


class ListenIpfsMetaTests(TestCase):
    def setUp(self):
        celeryapp.conf.update(CELERY_TASK_ALWAYS_EAGER=True)

    @patch('bdn.redis.get_redis', fake_get_redis(1))
    @patch('bdn.contract.contract', fake_hash_storage_contract([
        {
            'transactionHash': 1.0,
            'blockHash': 1.0,
            'blockNumber': '1',
            'args': {
                'ipfsHash': bytes('some_ipfs_hash', 'utf-8'),
                'grantedTo': 'granted_to',
            }
        },
        {
            'transactionHash': 1.0,
            'blockHash': 1.0,
            'blockNumber': '2',
            'args': {
                'ipfsHash': bytes('some_ipfs_hash', 'utf-8'),
                'grantedTo': 'granted_to',
            }
        }
    ]))
    def test_verification_task(self):
        listen_ethereum_ipfs_hash_storage()

    @patch('bdn.redis.get_redis', fake_get_redis(0))
    @patch('bdn.contract.contract', fake_hash_storage_contract([]))
    @patch('requests.get', fake_ipfs_request_get([]))
    def test_verification_task_zero_block(self):
        listen_ethereum_ipfs_hash_storage()


class PerformIpfsMetaTests(TestCase):
    def setUp(self):
        self.verifier, _ = User.objects.get_or_create(pk='3482b1bb-cb39-4fcd-91c2-690c48223a51')
        self.granted_to, _ = User.objects.get_or_create(username='0x04')
        self.certificate = Certificate(
            id='0cb19a83-d3c9-491b-99a3-374ebb01c43f',
            academy_title='test',
            academy_link='http://test.com/',
            course_title='test',
            learner_eth_address='0x0',
        )
        self.certificate.save()
        self.verification = Verification(pk='9ffd6ed3-fa64-4beb-903e-b1c4fd6d0c99',
            certificate=self.certificate, verifier=self.verifier, state='pending',
            verifier_type=2, granted_to_type=1)
        self.verification.save()

    @patch('requests.get', fake_ipfs_request_get([
        {
            'verifier': '3482b1bb-cb39-4fcd-91c2-690c48223a51',
            'id': '9ffd6ed3-fa64-4beb-903e-b1c4fd6d0c99',
            'certificate': {
                'id': '0cb19a83-d3c9-491b-99a3-374ebb01c43f',
            },
        }
    ]))
    def test_verification_task(self):
        perform_ipfs_meta_verification({
            'transactionHash': '0x03',
            'blockHash': '0x02',
            'blockNumber': '1',
            'args': {
                'ipfsHash': 'QWERTY',
                'grantedTo': '0x04',
                },
            })

    def test_no_ipfs_meta(self):
        with self.assertRaises(NoArgumentsError):
            perform_ipfs_meta_verification({
                'transactionHash': '0x03',
                'blockHash': '0x02',
                'blockNumber': '1',
                'args': {

                    },
                })
    @patch('requests.get', fake_ipfs_request_get([
        {
            None,
        }
    ]))
    def test_no_ipfs_data(self):
        with self.assertRaises(IpfsDataAttributeError):
            perform_ipfs_meta_verification({
                'transactionHash': '0x03',
                'blockHash': '0x02',
                'blockNumber': '1',
                'args': {
                    'ipfsHash': 'QWERTY',
                    'grantedTo': '0x04',
                    },
                })

    @patch('requests.get', fake_ipfs_request_get([
        {
            'verifier': '3482b1bb-cb39-4fcd-91c2-690c48223a51',
            'id': '9ffd6ed3-fa64-4beb-903e-b1c4fd6d0c99',
            'certificate': {
                'id': '0cb19a83-d3c9-491b-99a3-374ebb01c43f',
            },
        }
    ]))
    def test_granted_to_does_not_exist(self):
        with self.assertRaises(GrantedToUserDoesNotExist):
            perform_ipfs_meta_verification({
                'transactionHash': '0x03',
                'blockHash': '0x02',
                'blockNumber': '1',
                'args': {
                    'ipfsHash': 'QWERTY',
                    'grantedTo': 'someDoesNotExistingUsername',
                    },
                })

    @patch('requests.get', fake_ipfs_request_get([
        {
            'verifier': '4a066a6f-48e6-4e48-badd-addd90058571',
            'id': '9ffd6ed3-fa64-4beb-903e-b1c4fd6d0c99',
            'certificate': {
                'id': '0cb19a83-d3c9-491b-99a3-374ebb01c43f',
            },
        }
    ]))
    def test_verifier_does_not_exist(self):
        with self.assertRaises(VerifierUserDoesNotExist):
            perform_ipfs_meta_verification({
                'transactionHash': '0x03',
                'blockHash': '0x02',
                'blockNumber': '1',
                'args': {
                    'ipfsHash': 'QWERTY',
                    'grantedTo': '0x04',
                    },
                })

    @patch('requests.get', fake_ipfs_request_get([
        {
            'verifier': 'not_valid_id',
            'id': '9ffd6ed3-fa64-4beb-903e-b1c4fd6d0c99',
            'certificate': {
                'id': '0cb19a83-d3c9-491b-99a3-374ebb01c43f',
            },
        }
    ]))
    def test_verifier_not_valid_id(self):
        with self.assertRaises(VerifierUserValidationError):
            perform_ipfs_meta_verification({
                'transactionHash': '0x03',
                'blockHash': '0x02',
                'blockNumber': '1',
                'args': {
                    'ipfsHash': 'QWERTY',
                    'grantedTo': '0x04',
                    },
                })

    @patch('requests.get', fake_ipfs_request_get([
        {
            'verifier': '3482b1bb-cb39-4fcd-91c2-690c48223a51',
            'id': '0f3693ba-8288-4345-b306-d881ee49a58d',
            'certificate': {
                'id': '0cb19a83-d3c9-491b-99a3-374ebb01c43f',
            },
        }
    ]))
    def test_verification_does_not_exist(self):
        with self.assertRaises(VerificationDoesNotExist):
            perform_ipfs_meta_verification({
                'transactionHash': '0x03',
                'blockHash': '0x02',
                'blockNumber': '1',
                'args': {
                    'ipfsHash': 'QWERTY',
                    'grantedTo': '0x04',
                    },
                })

    @patch('requests.get', fake_ipfs_request_get([
        {
            'verifier': '3482b1bb-cb39-4fcd-91c2-690c48223a51',
            'id': 'not_valid_id',
            'certificate': {
                'id': '0cb19a83-d3c9-491b-99a3-374ebb01c43f',
            },
        }
    ]))
    def test_verification_not_valid_id(self):
        with self.assertRaises(VerificationValidationError):
            perform_ipfs_meta_verification({
                'transactionHash': '0x03',
                'blockHash': '0x02',
                'blockNumber': '1',
                'args': {
                    'ipfsHash': 'QWERTY',
                    'grantedTo': '0x04',
                    },
                })

    @patch('requests.get', fake_ipfs_request_get([
        {
            'verifier': '3482b1bb-cb39-4fcd-91c2-690c48223a51',
            'id': '9ffd6ed3-fa64-4beb-903e-b1c4fd6d0c99',
            'certificate': {
                'id': '0cb19a83-d3c9-491b-99a3-374ebb01c43f',
            },
        }
    ]))
    def test_verification_allready_verified(self):
        self.verification.state = 'verified'
        self.verification.save()
        perform_ipfs_meta_verification({
            'transactionHash': '0x03',
            'blockHash': '0x02',
            'blockNumber': '1',
            'args': {
                'ipfsHash': 'QWERTY',
                'grantedTo': '0x04',
                },
            })

    @patch('requests.get', fake_ipfs_request_get([
        {
            'verifier': '3482b1bb-cb39-4fcd-91c2-690c48223a51',
            'id': '9ffd6ed3-fa64-4beb-903e-b1c4fd6d0c99',
            'certificate': {
                'id': 'afbf9bfb-4380-486c-bdb6-902197904995',
            },
        }
    ]))
    def test_certificate_does_not_exist(self):
        with self.assertRaises(CertificateDoesNotExist):
            perform_ipfs_meta_verification({
                'transactionHash': '0x03',
                'blockHash': '0x02',
                'blockNumber': '1',
                'args': {
                    'ipfsHash': 'QWERTY',
                    'grantedTo': '0x04',
                    },
                })

    @patch('requests.get', fake_ipfs_request_get([
        {
            'verifier': '3482b1bb-cb39-4fcd-91c2-690c48223a51',
            'id': '9ffd6ed3-fa64-4beb-903e-b1c4fd6d0c99',
            'certificate': {
                'id': 'not_valid_id',
            },
        }
    ]))
    def test_certificate_not_valid_id(self):
        with self.assertRaises(CertificateValidationError):
            perform_ipfs_meta_verification({
                'transactionHash': '0x03',
                'blockHash': '0x02',
                'blockNumber': '1',
                'args': {
                    'ipfsHash': 'QWERTY',
                    'grantedTo': '0x04',
                    },
                })

    def tearDown(self):
        self.verification.delete()
        self.certificate.delete()
        self.verifier.delete()
        self.granted_to.delete()
