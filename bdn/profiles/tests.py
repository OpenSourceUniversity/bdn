# flake8: noqa

import uuid
from django.test import RequestFactory, TestCase
from bdn.auth.models import User
from .views import ProfileViewSet

class ProfileTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_profiles_create_and_then_get(self):
        # Create learner profile
        request = self.factory.post(
            '/api/v1/profile/',
            data={
                'first_name': 'test',
                'last_name': 'test',
                'learner_email': 'test@test.com',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735',
            HTTP_PROFILE_TYPE='1',
        )
        response = ProfileViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)

    # Create academy profile
        request = self.factory.post(
            '/api/v1/profile/',
            data={
                'academy_name': 'test',
                'academy_website': 'http://test.com',
                'learner_email': 'test@test.com',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735',
            HTTP_PROFILE_TYPE='2',
        )
        response = ProfileViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)

    # Create business profile
        request = self.factory.post(
            '/api/v1/profile/',
            data={
                'company_name': 'test',
                'company_website': 'http://test.com',
                'company_email': 'test@test.com',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735',
            HTTP_PROFILE_TYPE='3',
        )
        response = ProfileViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)

    # Get profile
        request = self.factory.get(
            '/api/v1/profile/',
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735',
        )
        response = ProfileViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)

        eth_address = '0xD2BE64317Eb1832309DF8c8C18B09871809f3735'.lower()
        user, _ = User.objects.get_or_create(username=eth_address)
    # Get learner profile
        request = self.factory.get(
                '/api/v1/profile/{}/get_learner/'.format(user.username),
                HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
                HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735',
            )
        response = ProfileViewSet.as_view({'get': 'get_learner'})(request, pk=user.username)
        self.assertEqual(response.status_code, 200)

    # Get academies
        request = self.factory.get(
                '/api/v1/profile/get_academies/',
                HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
                HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735',
            )
        response = ProfileViewSet.as_view({'get': 'get_academies'})(request)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    # Get businesses
        request = self.factory.get(
                '/api/v1/profile/get_businesses/',
                HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
                HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735',
            )
        response = ProfileViewSet.as_view({'get': 'get_businesses'})(request)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    # Get learners
        request = self.factory.get(
                '/api/v1/profile/get_learners/',
                HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
                HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735',
            )
        response = ProfileViewSet.as_view({'get': 'get_learners'})(request)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

    #Set active profile
        request = self.factory.post(
            '/api/v1/profile/set_active_profile/',
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735',
            HTTP_PROFILE_TYPE='3',
        )
        response = ProfileViewSet.as_view({'post': 'set_active_profile'})(request)
        self.assertEqual(response.status_code, 200)
    # Get active profile
        request = self.factory.get(
                '/api/v1/profile/get_active_profile/',
                HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
                HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735',
            )
        response = ProfileViewSet.as_view({'get': 'get_active_profile'})(request)
        self.assertEqual(response.data.get('active_profile_type'), 3)
        self.assertEqual(response.status_code, 200)

        user.profile.public_profile = False
        user.profile.save()
    # Get private learner profile
        request = self.factory.get(
                '/api/v1/profile/{}/get_learner/'.format(user.username),
                HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
                HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735',
            )
        response = ProfileViewSet.as_view({'get': 'get_learner'})(request, pk=user.username)
        self.assertEqual(response.status_code, 403)

