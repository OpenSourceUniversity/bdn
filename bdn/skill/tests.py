# flake8: noqa

import uuid
from django.test import RequestFactory, TestCase
from bdn.auth.models import User
from .models import Skill
from .views import SkillViewSet


class SkillTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_course_create_and_then_delete_it(self):
        eth_address = '0xD2BE64317Eb1832309DF8c8C18B09871809f3735'.lower()
        user, _ = User.objects.get_or_create(username=eth_address)
        skill, _ = Skill.objects.get_or_create(name='skill', standardized=True)
        # Get skill autocomplete
        request = self.factory.get(
            '/api/v1/skills/autocomplete?q=skill',
            data={
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = SkillViewSet.as_view({'get': 'autocomplete'})(request)
        self.assertEqual(response.status_code, 200)

        # Get skill autocomplete no query
        request = self.factory.get(
            '/api/v1/skills/autocomplete',
            data={
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = SkillViewSet.as_view({'get': 'autocomplete'})(request)
        self.assertEqual(response.status_code, 200)