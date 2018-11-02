# flake8: noqa

import uuid
from django.test import RequestFactory, TestCase
from bdn.auth.models import User
from .models import Thread
from .views import ThreadViewSet, MessageViewSet


class MessagingTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_create_get_list_delete_thread(self):
        # Create new thread
        eth_address = '0xD2BE64317Eb1832309DF8c8C18B09871809f3735'.lower()
        user, _ = User.objects.get_or_create(username=eth_address)
        opponent_eth_address = '0xD2BE64317Eb1832309DF8c8C18B09871809f3739'.lower()
        opponent, _ = User.objects.get_or_create(username=opponent_eth_address)
        wrong_user_eth_address = '0xD2BE64317Eb1832309DF8c8C18B09871809f3736'.lower()
        wrong_user, _ = User.objects.get_or_create(username=wrong_user_eth_address)
        request = self.factory.post(
            '/api/v1/messaging/threads/',
            data={
                'opponent_eth_address': '0xD2BE64317Eb1832309DF8c8C18B09871809f3739',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = ThreadViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)
        thread_pk = str(response.data['id'])

        # Get created thread
        request = self.factory.post(
            '/api/v1/messaging/threads/',
            data={
                'opponent_eth_address': '0xD2BE64317Eb1832309DF8c8C18B09871809f3739',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = ThreadViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)

        # Opponent doesn't exist
        request = self.factory.post(
            '/api/v1/messaging/threads/',
            data={
                'opponent_eth_address': '0xD2BE64317Eb1832309DF8c8C18B09871809f3730',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = ThreadViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)

        # Get threads list
        request = self.factory.get(
            '/api/v1/messaging/threads/',
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = ThreadViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)

        # Get unread count
        request = self.factory.get(
            '/api/v1/messaging/threads/get_unread_count/',
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = ThreadViewSet.as_view({'get': 'get_unread_count'})(request)
        self.assertEqual(response.data['unread_messages_count'], 0)

        testing_thread = Thread.objects.get(pk=thread_pk)
        testing_thread.owner = wrong_user
        testing_thread.save()

        # Delete Thread deny
        request = self.factory.delete(
            '/api/v1/messaging/threads/{}/'.format(thread_pk),
            data={
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        view = ThreadViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=thread_pk)
        self.assertEqual(response.status_code, 401)

        testing_thread.owner = user
        testing_thread.save()

        # Delete Thread
        request = self.factory.delete(
            '/api/v1/messaging/threads/{}/'.format(thread_pk),
            data={
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        view = ThreadViewSet.as_view({'delete': 'destroy'})
        response = view(request, pk=thread_pk)
        self.assertEqual(response.status_code, 200)


    def test_create_get_list_message(self):
        # Create new thread
        eth_address = '0xD2BE64317Eb1832309DF8c8C18B09871809f3735'.lower()
        user, _ = User.objects.get_or_create(username=eth_address)
        opponent_eth_address = '0xD2BE64317Eb1832309DF8c8C18B09871809f3739'.lower()
        opponent, _ = User.objects.get_or_create(username=opponent_eth_address)
        request = self.factory.post(
            '/api/v1/messaging/threads/',
            data={
                'opponent_eth_address': '0xD2BE64317Eb1832309DF8c8C18B09871809f3739',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = ThreadViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)
        thread_pk = str(response.data['id'])

        # Get messages list
        request = self.factory.get(
            '/api/v1/messages/?thread_id={}'.format(thread_pk),
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = MessageViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)

        # Get messages list thread does not exist
        wrong_id = str(uuid.uuid4())
        request = self.factory.get(
            '/api/v1/messages/?thread_id={}'.format(wrong_id),
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = MessageViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 404)

        # Create message with wrong data
        request = self.factory.post(
            '/api/v1/messages/',
            data={
                'threadID': thread_pk,
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = MessageViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)

        # Create message
        request = self.factory.post(
            '/api/v1/messages/',
            data={
                'threadID': thread_pk,
                'text': 'test',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = MessageViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)
        message_pk = str(response.data['id'])

        # Mark as read message
        mark_as_read_url = '/api/v1/messages/{}/mark_as_read_by_id/'.format(message_pk)
        request = self.factory.post(
            mark_as_read_url,
            data={
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        view = MessageViewSet.as_view({'post': 'mark_as_read_by_id'})
        response = view(request, pk=message_pk)
        self.assertEqual(response.status_code, 200)
