# flake8: noqa

import uuid
from django.test import RequestFactory, TestCase
from bdn.auth.models import User
from bdn.provider.models import Provider
from .views import CourseViewSet


class CourseTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_course_create_and_then_delete_it(self):
        # Create course with error (provider not found)
        request = self.factory.post(
            '/api/v1/courses/',
            data={
                'title': 'test',
                'description': 'test',
                'external_link': 'http://example.com/',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = CourseViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)

        # Create course
        eth_address = '0xD2BE64317Eb1832309DF8c8C18B09871809f3735'.lower()
        user, _ = User.objects.get_or_create(username=eth_address)
        provider = Provider(user=user, name='test')
        provider.save()
        request = self.factory.post(
            '/api/v1/courses/',
            data={
                'title': 'test',
                'description': 'test',
                'external_link': 'http://example.com/',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = CourseViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)
        course_pk = str(response.data['pk'])

        # Create wrong course (invalid data)
        request = self.factory.post(
            '/api/v1/courses/',
            data={
                'title': '',
                'description': 'test',
                'external_link': 'http://example.com/',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = CourseViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)

        # Retrieve the course
        request = self.factory.get(
            '/api/v1/courses/{}/'.format(course_pk),
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')
        response = CourseViewSet.as_view({'get': 'retrieve'})(request, pk=course_pk)
        self.assertEqual(response.status_code, 200)

        wrong_pk = str(uuid.uuid4())
        request = self.factory.get(
            '/api/v1/courses/{}/'.format(wrong_pk),
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')
        view = CourseViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=wrong_pk)
        self.assertEqual(response.status_code, 404)

        # Listing
        industry_pks = '1427837e-babf-42c8-98ce-3517cb768249|some_wrong_uuid||'
        request = self.factory.get(
            '/api/v1/courses/?filter_industry={}&is_featured=1'.format(industry_pks),
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')
        view = CourseViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

        # Get by provider
        request = self.factory.get(
            '/api/v1/courses/get_by_provider/?eth_address={}'.format(
                user.username),
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')
        view = CourseViewSet.as_view({'get': 'get_by_provider'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

        # Search
        request = self.factory.get(
            '/api/v1/courses/?q=python',
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')
        view = CourseViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.get(
            '/api/v1/courses/search/?q=python',
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')
        view = CourseViewSet.as_view({'get': 'search'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.get(
            '/api/v1/courses/autocomplete/?q=autocomplete',
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')
        view = CourseViewSet.as_view({'get': 'autocomplete'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

        # Get course by id
        request = self.factory.get(
            '/api/v1/courses/{}/get_by_id/'.format(course_pk),
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')
        view = CourseViewSet.as_view({'get': 'get_by_id'})
        response = view(request, pk=course_pk)
        self.assertEqual(response.status_code, 200)

        wrong_pk = str(uuid.uuid4())
        request = self.factory.get(
            '/api/v1/courses/{}/get_by_id/'.format(wrong_pk),
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')
        view = CourseViewSet.as_view({'get': 'get_by_id'})
        response = view(request, pk=wrong_pk)
        self.assertEqual(response.status_code, 404)

        # Edit the course
        request = self.factory.post(
            '/api/v1/courses/{}/edit_by_id/'.format(course_pk),
            data={
                'title': 'test editted',
                'description': 'test',
                'external_link': 'http://example.com/',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        view = CourseViewSet.as_view({'post': 'edit_by_id'})
        response = view(request, pk=course_pk)
        self.assertEqual(response.status_code, 200)

        # Delete it
        url = '/api/v1/courses/{}/delete_by_id/'.format(course_pk)
        request = self.factory.post(
            url,
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')
        view = CourseViewSet.as_view({'post': 'delete_by_id'})
        response = view(request, pk=course_pk)
        self.assertEqual(response.status_code, 200)
