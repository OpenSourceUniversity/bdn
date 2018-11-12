# flake8: noqa

import uuid
from unittest.mock import MagicMock, patch
from django.test import RequestFactory, TestCase
from bdn.auth.models import User
from bdn.celery import app as celeryapp
from bdn.utils.send_email_tasks import inviting_email
from .tasks import handle_connection_row
from .views import FileViewSet


class fake_get_redis:
    def __init__(self, get_result):
        self._get_result = get_result

    def __call__(self):
        mock = MagicMock()
        mock.get.return_value = self._get_result
        return mock

class ConnectionTasksTests(TestCase):
    def setUp(self):
        celeryapp.conf.update(CELERY_TASK_ALWAYS_EAGER=True)
        self.eth_address = '0xD2BE64317Eb1832309DF8c8C18B09871809f3735'.lower()
        self.user, _ = User.objects.get_or_create(username=self.eth_address, email='test@email.com')

    @patch('bdn.redis.get_redis', fake_get_redis(1))

    def test_connection_row_task(self):
        handle_connection_row(
            str(self.user.id),
            ['first', 'second', 'test@email.com', 'company', 'position', '5/8/18, 11:30 AM' ]
            )

    def test_connection_without_email_row_task(self):
        handle_connection_row(
            str(self.user.id),
            ['first', 'second', '', 'company', 'position', '5/8/18, 11:30 AM' ]
            )

    def test_connection_row_duplicate_task(self):
        handle_connection_row(
            str(self.user.id),
            ['first', 'second', 'test@email.com', 'company', 'position', '5/8/18, 11:30 AM' ]
            )
        handle_connection_row(
            str(self.user.id),
            ['first', 'second', 'test@email.com', 'company', 'position', '5/8/18, 11:30 AM' ]
            )

    def test_connection_row_user_not_onboarded_task(self):
        handle_connection_row(
            str(self.user.id),
            ['first', 'second', 'test2@email.com', 'company', 'position', '5/8/18, 11:30 AM' ]
            )

    def test_connection_send_email_task(self):
        connection = {}
        connection['full_name'] = 'test'
        connection['email'] = 'test2@email.com'
        inviting_email(
            connection,
            'https://os.university',
            'test@email.com'
            )

class ConnectionViewsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.eth_address = '0xD2BE64317Eb1832309DF8c8C18B09871809f3735'.lower()
        self.user, _ = User.objects.get_or_create(username=self.eth_address, email='test@email.com')

    def test_file_upload(self):
        with open('test_files/test_connections.zip', 'rb') as connections:
            # Create User Settings
            request = self.factory.post(
                '/api/v1/user-settings/',
                data={
                },
                HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
                HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
            )
            request.FILES['datafile'] = connections
            request.FILES['datafile'].read()
            response = FileViewSet.as_view({'post': 'create'})(request)
            self.assertEqual(response.status_code, 200)

