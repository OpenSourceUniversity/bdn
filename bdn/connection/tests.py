# flake8: noqa

import uuid
from unittest.mock import MagicMock, patch
from django.test import RequestFactory, TestCase
from bdn.auth.models import User
from bdn.celery import app as celeryapp
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

    def test_connection_row_user_not_onboarded_task(self):
        handle_connection_row(
            str(self.user.id),
            ['first', 'second', 'test2@email.com', 'company', 'position', '5/8/18, 11:30 AM' ]
            )
