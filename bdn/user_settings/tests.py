# flake8: noqa

import uuid
from django.test import RequestFactory, TestCase
from bdn.auth.models import User
from .models import UserSettings
from .views import UserSettingsViewSet


class UserSettingsTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_create_get_user_settings(self):
        # Create new job position
        eth_address = '0xD2BE64317Eb1832309DF8c8C18B09871809f3735'.lower()
        user, _ = User.objects.get_or_create(username=eth_address, email='test@email.com')
        second_eth_address = '0xD2BE64317Eb1832309DF8c8C18B09871809f3739'.lower()
        duplicate_email = 'duplicate@email.com'
        user_duplicate, _ = User.objects.get_or_create(username=second_eth_address, email=duplicate_email)

        # Create User Settings
        request = self.factory.post(
            '/api/v1/user-settings/',
            data={
                'subscribed': True,
                'news_subscribed': True,
                'email': 'test@email.com',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = UserSettingsViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)

        # Duplicate User email
        request = self.factory.post(
            '/api/v1/user-settings/',
            data={
                'subscribed': True,
                'news_subscribed': True,
                'email': duplicate_email,
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = UserSettingsViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)

        # Change User email
        request = self.factory.post(
            '/api/v1/user-settings/',
            data={
                'subscribed': True,
                'news_subscribed': True,
                'email': 'test2@email.com',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = UserSettingsViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)

        # Serializer create error
        request = self.factory.post(
            '/api/v1/user-settings/',
            data={
                'subscribed': 'Wrong_format',
                'news_subscribed': True,
                'email': 'test2@email.com',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = UserSettingsViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)

        # Get user settings
        request = self.factory.get(
            '/api/v1/user-settings/',
            data={
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = UserSettingsViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)

        # Save wallet with Recovery
        request = self.factory.post(
            '/api/v1/user-settings/set_wallet/',
            data={
                'email': 'test2@email.com',
                'isRecovery': True,
                'password': 'test',
                'wallet': 'test',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = UserSettingsViewSet.as_view({'post': 'set_wallet'})(request)
        self.assertEqual(response.status_code, 200)

        user.usersettings.save_wallet = False
        user.usersettings.save()

        # Delete wallet with Recovery
        request = self.factory.post(
            '/api/v1/user-settings/set_wallet/',
            data={
                'email': 'test2@email.com',
                'password': 'test',
                'wallet': 'test',
                'isRecovery': True,
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = UserSettingsViewSet.as_view({'post': 'set_wallet'})(request)
        self.assertEqual(response.status_code, 200)

        # Delete wallet 
        request = self.factory.post(
            '/api/v1/user-settings/set_wallet/',
            data={
                'email': 'test2@email.com',
                'password': 'test',
                'wallet': 'test',
                'save_wallet': False,
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = UserSettingsViewSet.as_view({'post': 'set_wallet'})(request)
        self.assertEqual(response.status_code, 200)

        user.usersettings.save_wallet = True
        user.usersettings.save()

        # Save wallet 
        request = self.factory.post(
            '/api/v1/user-settings/set_wallet/',
            data={
                'email': 'test2@email.com',
                'password': 'test',
                'wallet': 'test',
                'save_wallet': True,
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = UserSettingsViewSet.as_view({'post': 'set_wallet'})(request)
        self.assertEqual(response.status_code, 200)

        # Get wallet 
        request = self.factory.post(
            '/api/v1/user-settings/get_wallet/',
            data={
                'email': 'test2@email.com',
                'password': 'test',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = UserSettingsViewSet.as_view({'post': 'get_wallet'})(request)
        self.assertEqual(response.status_code, 200)

        # Get wallet wrong password
        request = self.factory.post(
            '/api/v1/user-settings/get_wallet/',
            data={
                'email': 'test2@email.com',
                'password': 'wrong_password',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = UserSettingsViewSet.as_view({'post': 'get_wallet'})(request)
        self.assertEqual(response.status_code, 400)

        user.usersettings.wallet = None
        user.usersettings.password = None
        user.usersettings.save()

        # Get wallet not stored
        request = self.factory.post(
            '/api/v1/user-settings/get_wallet/',
            data={
                'email': 'test2@email.com',
                'password': 'wrong_password',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = UserSettingsViewSet.as_view({'post': 'get_wallet'})(request)
        self.assertEqual(response.status_code, 400)

         # Get wallet not stored without email
        request = self.factory.post(
            '/api/v1/user-settings/get_wallet/',
            data={
                'email': '',
                'password': 'password',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = UserSettingsViewSet.as_view({'post': 'get_wallet'})(request)
        self.assertEqual(response.status_code, 400)


