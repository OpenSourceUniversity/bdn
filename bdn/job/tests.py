# flake8: noqa

import uuid
from django.test import RequestFactory, TestCase
from bdn.auth.models import User
from bdn.company.models import Company
from .views import JobViewSet


class JobTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_job_create_and_then_delete_it(self):
        # Create job with error (company not found)
        request = self.factory.post(
            '/api/v1/jobs/',
            data={
                'title': 'test',
                'location': 'test',
                'overview': 'test',
                'description': 'test',
                'hours': 'test',
                'external_link': 'http://example.com/',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = JobViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)

        # Create job
        eth_address = '0xD2BE64317Eb1832309DF8c8C18B09871809f3735'.lower()
        user, _ = User.objects.get_or_create(username=eth_address)
        have_allowance = True
        try:
            user.allowance.featured_jobs = 1
            user.allowance.save()
        except AttributeError:
            have_allowance = False
        company = Company(user=user, name='test')
        company.save()
        request = self.factory.post(
            '/api/v1/jobs/',
            data={
                'title': 'test',
                'location': 'test',
                'overview': 'test',
                'description': 'test',
                'hours': 1,
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = JobViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)
        job_pk = str(response.data['pk'])

        # Create wrong job (invalid data)
        request = self.factory.post(
            '/api/v1/jobs/',
            data={
                'title': '',
                'location': 'test',
                'overview': 'test',
                'description': 'test',
                'hours': 'test',
                'external_link': 'http://example.com/',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = JobViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)

        # Retrieve the job
        request = self.factory.get(
            '/api/v1/jobs/{}/'.format(job_pk),
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')
        response = JobViewSet.as_view({'get': 'retrieve'})(request, pk=job_pk)
        self.assertEqual(response.status_code, 200)

        wrong_pk = str(uuid.uuid4())
        request = self.factory.get(
            '/api/v1/jobs/{}/'.format(wrong_pk),
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')
        view = JobViewSet.as_view({'get': 'retrieve'})
        response = view(request, pk=wrong_pk)
        self.assertEqual(response.status_code, 404)

        # Listing
        industry_pks = '1427837e-babf-42c8-98ce-3517cb768249|some_wrong_uuid||'
        request = self.factory.get(
            '/api/v1/jobs/?filter_industry={}&is_featured=1'.format(industry_pks),
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')
        view = JobViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

        # Get by company
        request = self.factory.get(
            '/api/v1/jobs/get_by_company/?eth_address={}'.format(
                user.username),
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')
        view = JobViewSet.as_view({'get': 'get_by_company'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

        # Search
        request = self.factory.get(
            '/api/v1/jobs/?q=python',
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')
        view = JobViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.get(
            '/api/v1/jobs/search/?q=python',
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')
        view = JobViewSet.as_view({'get': 'search'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

        request = self.factory.get(
            '/api/v1/jobs/autocomplete/?q=autocomplete',
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')
        view = JobViewSet.as_view({'get': 'autocomplete'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

        # Get job by id
        request = self.factory.get(
            '/api/v1/jobs/{}/get_by_id/'.format(job_pk),
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')
        view = JobViewSet.as_view({'get': 'get_by_id'})
        response = view(request, pk=job_pk)
        self.assertEqual(response.status_code, 200)

        wrong_pk = str(uuid.uuid4())
        request = self.factory.get(
            '/api/v1/jobs/{}/get_by_id/'.format(wrong_pk),
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')
        view = JobViewSet.as_view({'get': 'get_by_id'})
        response = view(request, pk=wrong_pk)
        self.assertEqual(response.status_code, 404)

        # Edit the job with wrong company
        wrong_username = '0xD2BE64317Eb1832309DF8c8C18B09871809f3736'.lower()
        wrong_user, _ = User.objects.get_or_create(username=wrong_username)
        company.user = wrong_user
        company.save()
        request = self.factory.post(
            '/api/v1/jobs/{}/edit_by_id/'.format(job_pk),
            data={
                'title': 'test editted',
                'description': 'test',
                'external_link': 'http://example.com/',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        view = JobViewSet.as_view({'post': 'edit_by_id'})
        response = view(request, pk=job_pk)
        self.assertEqual(response.status_code, 401)

        # Edit the job
        company.user = user
        company.save()
        request = self.factory.post(
            '/api/v1/jobs/{}/edit_by_id/'.format(job_pk),
            data={
                'title': 'test editted',
                'description': 'test',
                'external_link': 'http://example.com/',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        view = JobViewSet.as_view({'post': 'edit_by_id'})
        response = view(request, pk=job_pk)
        self.assertEqual(response.status_code, 200)

        # Edit the job with serializer error
        request = self.factory.post(
            '/api/v1/jobs/{}/edit_by_id/'.format(job_pk),
            data={
                'title': '',
                'description': 'test',
                'external_link': 'http://example.com/',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        view = JobViewSet.as_view({'post': 'edit_by_id'})
        response = view(request, pk=job_pk)
        self.assertEqual(response.status_code, 400)

        # Mark as feautered
        request = self.factory.post(
            '/api/v1/jobs/{}/mark_featured_by_id/'.format(job_pk),
            data={
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        view = JobViewSet.as_view({'post': 'mark_featured_by_id'})
        response = view(request, pk=job_pk)
        self.assertEqual(response.status_code, 200)

        if have_allowance:
            request = self.factory.post(
                '/api/v1/jobs/',
                data={
                    'title': 'test2',
                    'location': 'test2',
                    'overview': 'test2',
                    'description': 'test2',
                    'hours': 2,
                },
                HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
                HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
            )
            response = JobViewSet.as_view({'post': 'create'})(request)
            self.assertEqual(response.status_code, 200)
            job_pk = str(response.data['pk'])

            request = self.factory.post(
                '/api/v1/jobs/{}/mark_featured_by_id/'.format(job_pk),
                data={
                },
                HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
                HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
            )
            view = JobViewSet.as_view({'post': 'mark_featured_by_id'})
            response = view(request, pk=job_pk)
            self.assertEqual(response.status_code, 400)

        # Delete denied
        company.user = wrong_user
        company.save()
        url = '/api/v1/jobs/{}/delete_by_id/'.format(job_pk)
        request = self.factory.post(
            url,
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')
        view = JobViewSet.as_view({'post': 'delete_by_id'})
        response = view(request, pk=job_pk)
        self.assertEqual(response.status_code, 401)

        # Delete it
        company.user = user
        company.save()
        url = '/api/v1/jobs/{}/delete_by_id/'.format(job_pk)
        request = self.factory.post(
            url,
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')
        view = JobViewSet.as_view({'post': 'delete_by_id'})
        response = view(request, pk=job_pk)
        self.assertEqual(response.status_code, 200)