# flake8: noqa

from django.test import RequestFactory, TestCase

from .views import CertificateViewSet


class CertificateTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

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
