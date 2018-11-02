# flake8: noqa

import uuid
from django.test import RequestFactory, TestCase
from bdn.auth.models import User
from .views import TransactionViewSet


class TransactionTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_create_list_transaction(self):
        # Create new transaction
        eth_address = '0xD2BE64317Eb1832309DF8c8C18B09871809f3735'.lower()
        user, _ = User.objects.get_or_create(username=eth_address)
        request = self.factory.post(
            '/api/v1/transactions/',
            data={
                'value': 1,
                'receiver': eth_address,
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = TransactionViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)

        # Create new transaction serializer error
        request = self.factory.post(
            '/api/v1/transactions/',
            data={
                'receiver': eth_address,
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = TransactionViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)
        # List transactions
        request = self.factory.get(
            '/api/v1/transactions/',
            data={
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = TransactionViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)

