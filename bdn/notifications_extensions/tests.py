# flake8: noqa

import uuid
from django.test import RequestFactory, TestCase
from bdn.auth.models import User
from notifications.models import Notification
from notifications.signals import notify
from .views import NotificationViewSet


class NotificationTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_get_list_notifications(self):
        eth_address = '0xD2BE64317Eb1832309DF8c8C18B09871809f3735'.lower()
        user, _ = User.objects.get_or_create(username=eth_address)
        notify.send(
            user,
            recipient=user,
            verb='requested',
            action_object=user,
        )

        # List notification
        request = self.factory.get(
            '/api/v1/notifications/',
            data={
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = NotificationViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)
        notification_id = response.data['results'][0]['id']

        # Get notification
        request = self.factory.get(
            '/api/v1/notifications/{}/'.format(notification_id),
            data={
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        view = NotificationViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=notification_id)
        self.assertEqual(response.status_code, 200)

        # Toggle unread notification
        request = self.factory.post(
            '/api/v1/notifications/{}/toggle_unread/'.format(notification_id),
            data={
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        view = NotificationViewSet.as_view({'post': 'toggle_unread'})
        response = view(request, pk=notification_id)
        self.assertEqual(response.status_code, 200)