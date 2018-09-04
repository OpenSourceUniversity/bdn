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

    def test_certificate_serializer_to_internal_value(self):
        serializer = CertificateSerializer(data={
            'academy_title': 'test',
            'academy_link': 'http://example.com',
            'course_title': 'test',
            'learner_eth_address': '0x0',
            'score': '',
            'duration': '',
        })
        self.assertTrue(serializer.is_valid())
        serializer = CertificateSerializer(data={
            'academy_title': 'test',
            'academy_link': 'http://example.com',
            'course_title': 'test',
            'learner_eth_address': '0x0',
            'score': 100,
            'duration': 100,
        })
        self.assertTrue(serializer.is_valid())


class CertificateViewProfileSerializerTests(TestCase):
    def test_verifications(self):
        certificate = Certificate(**{
            'academy_title': 'test',
            'academy_link': 'http://example.com',
            'course_title': 'test',
            'learner_eth_address': '0x0',
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
            'academy_title': 'test',
            'academy_link': 'http://example.com',
            'course_title': 'test',
            'learner_eth_address': '0x0',
            'expiration_date': timezone.now() - timedelta(hours=24)
        })
        certificate.save()
        serializer = CertificateViewProfileSerializer(certificate)
        self.assertTrue(serializer._is_expired(certificate))
