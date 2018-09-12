# flake8: noqa

from django.test import RequestFactory, TestCase
from django.utils import timezone
from datetime import timedelta
from bdn.verification.models import Verification
from bdn.auth.models import User
from .views import CertificateViewSet
from .apps import CertificateConfig
from .serializers import (
    CertificateSerializer, CertificateViewProfileSerializer)
from .models import Certificate


class CertificateTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_app_name(self):
        self.assertEqual(CertificateConfig.name, 'certificate')

    def test_auth_failure(self):
        request = self.factory.get('/api/v1/certificates/')
        response = CertificateViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(
            response.data['detail'],
            'Authentication credentials were not provided.')
        self.assertEqual(response.status_code, 403)

    def test_auth_success_and_list(self):
        request = self.factory.get(
            '/api/v1/certificates/',
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = CertificateViewSet.as_view({'get': 'list'})(request)
        self.assertEqual(response.status_code, 200)

    def test_certificate_create_and_then_delete_it(self):
        # Create certificate
        user, _ = User.objects.get_or_create(username='0x0')
        request = self.factory.post(
            '/api/v1/certificates/',
            data={
                'institution_title': 'test',
                'institution_link': 'http://example.com',
                'certificate_title': 'test',
                'holder_eth_address': '0xD2BE64317Eb1832309DF8c8C18B09871809f3735',
                'score': '',
                'duration': '',
                'skills': ['Python'],
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = CertificateViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)
        certificate_pk = str(response.data['certificate_pk'])

        # Retrieve the certificate
        request = self.factory.get(
            '/api/v1/certificates/{}/'.format(certificate_pk),
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')
        response = CertificateViewSet.as_view({'get': 'retrieve'})(request, pk=certificate_pk)
        self.assertEqual(response.status_code, 200)

        # Get certificates by learner
        request = self.factory.get(
            '/api/v1/certificates/get_certificates_by_learner/'\
            '?eth_address=0xD2BE64317Eb1832309DF8c8C18B09871809f3735',
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')
        view = CertificateViewSet.as_view({'get': 'get_certificates_by_learner'})
        response = view(request)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.status_code, 200)

        # Delete it
        url = '/api/v1/certificates/{}/delete_by_id/'.format(certificate_pk)
        request = self.factory.post(
            url,
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')
        view = CertificateViewSet.as_view({'post': 'delete_by_id'})
        response = view(request, pk=certificate_pk)
        self.assertEqual(response.status_code, 200)

    def test_delete_certificate_not_holded_by_user(self):
        User.objects.get_or_create(username='0x0')
        certificate = Certificate(**{
            'institution_title': 'test',
            'institution_link': 'http://example.com',
            'certificate_title': 'test',
        })
        certificate.save()
        url = '/api/v1/certificates/{}/delete_by_id/'.format(certificate.pk)
        request = self.factory.post(
            url,
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735')
        view = CertificateViewSet.as_view({'post': 'delete_by_id'})
        response = view(request, pk=certificate.pk)
        self.assertEqual(response.status_code, 401)

    def test_certificate_create_not_valid_data(self):
        user, _ = User.objects.get_or_create(username='0x0')
        request = self.factory.post(
            '/api/v1/certificates/',
            data={
                'institution_title': 'test',
                'institution_link': 'httttp://example.com',
                'certificate_title': 'test',
                'holder_eth_address': '0x0',
                'score': '',
                'duration': '',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = CertificateViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)

    def test_certificate_create_no_such_holder(self):
        request = self.factory.post(
            '/api/v1/certificates/',
            data={
                'institution_title': 'test',
                'institution_link': 'http://example.com',
                'certificate_title': 'test',
                'holder_eth_address': '0x1',
                'score': '',
                'duration': '',
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = CertificateViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)

    def test_certificate_serializer_to_internal_value(self):
        serializer = CertificateSerializer(data={
            'institution_title': 'test',
            'institution_link': 'http://example.com',
            'certificate_title': 'test',
            'score': '',
            'duration': '',
        })
        self.assertTrue(serializer.is_valid())
        serializer = CertificateSerializer(data={
            'institution_title': 'test',
            'institution_link': 'http://example.com',
            'certificate_title': 'test',
            'score': 100,
            'duration': 100,
        })
        self.assertTrue(serializer.is_valid())


class CertificateViewProfileSerializerTests(TestCase):
    def test_verifications(self):
        certificate = Certificate(**{
            'institution_title': 'test',
            'institution_link': 'http://example.com',
            'certificate_title': 'test',
        })
        certificate.save()
        verifier, _ = User.objects.get_or_create(email='verifier@example.com')
        verification = Verification(
            certificate=certificate,
            state='verified',
            verifier=verifier
        )
        verification.save()
        serializer = CertificateViewProfileSerializer(certificate)
        self.assertEqual(len(serializer._verifications(certificate)), 1)
        self.assertIsNone(serializer._is_expired(certificate))

    def test_certificate_expired(self):
        certificate = Certificate(**{
            'institution_title': 'test',
            'institution_link': 'http://example.com',
            'certificate_title': 'test',
            'expiration_date': timezone.now() - timedelta(hours=24)
        })
        certificate.save()
        serializer = CertificateViewProfileSerializer(certificate)
        self.assertTrue(serializer._is_expired(certificate))
