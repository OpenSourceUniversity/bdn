# flake8: noqa

import uuid
from django.test import RequestFactory, TestCase
from bdn.auth.models import User
from bdn.job.models import Job
from bdn.job.views import JobViewSet
from bdn.company.models import Company
from .models import JobApplication
from .views import JobApplicationViewSet


class JobApplicationTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_create_get_list_reject_job_application(self):
        # Create new job position
        eth_address = '0xD2BE64317Eb1832309DF8c8C18B09871809f3735'.lower()
        user, _ = User.objects.get_or_create(username=eth_address)
        company_user_eth_address = '0xD2BE64317Eb1832309DF8c8C18B09871809f3739'.lower()
        company_user, _ = User.objects.get_or_create(username=company_user_eth_address)
        company = Company(user=user, name='test')
        company.save()
        job = Job(title='test123', location='test', overview='test', description='test', hours=1, company=company)
        job.save()
        job_pk = str(job.id)

        # Create job application
        request = self.factory.post(
            '/api/v1/job-applications/',
            data={
                'job': job_pk,
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = JobApplicationViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)
        job_application_pk = str(response.data['id'])

        # Create duplicate job application
        request = self.factory.post(
            '/api/v1/job-applications/',
            data={
                'job': job_pk,
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = JobApplicationViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)

        # Get list
        request = self.factory.get(
            '/api/v1/job-applications/',
            data={
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = JobApplicationViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)

        # Get by user
        request = self.factory.get(
            '/api/v1/job-applications/get_by_user/',
            data={
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = JobApplicationViewSet.as_view({'get': 'get_by_user'})(request)
        self.assertEqual(response.status_code, 200)

        # Get by user and job
        request = self.factory.get(
            '/api/v1/job-applications/{}/get_by_user_and_job/'.format(job_pk),
            data={
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        view = JobApplicationViewSet.as_view({'get': 'get_by_user_and_job'})
        response = view(request, pk=job_pk)
        self.assertEqual(response.status_code, 200)

        # Change state by id reject
        request = self.factory.post(
            '/api/v1/job-applications/{}/change_state_by_id/?state={}'.format(job_application_pk, 'reject'),
            data={
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        view = JobApplicationViewSet.as_view({'post': 'change_state_by_id'})
        response = view(request, pk=job_application_pk)
        self.assertEqual(response.status_code, 200)

        job_application = JobApplication.objects.get(pk=job_application_pk)
        job_application.state = 'requested'
        job_application.save()

        # Change state by id approve
        request = self.factory.post(
            '/api/v1/job-applications/{}/change_state_by_id/?state={}'.format(job_application_pk, 'approve'),
            data={
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        view = JobApplicationViewSet.as_view({'post': 'change_state_by_id'})
        response = view(request, pk=job_application_pk)
        self.assertEqual(response.status_code, 200)

        company.user = company_user
        company.save()

        # Change state by id deny
        request = self.factory.post(
            '/api/v1/job-applications/{}/change_state_by_id/?state={}'.format(job_application_pk, 'approve'),
            data={
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        view = JobApplicationViewSet.as_view({'post': 'change_state_by_id'})
        response = view(request, pk=job_application_pk)
        self.assertEqual(response.status_code, 401)

