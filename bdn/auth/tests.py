# flake8: noqa

import unittest
from bdn.auth.models import User
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import AnonymousUser
from .signature_auth_middleware import SignatureAuthMiddleware
from .signature_authentication import SignatureAuthentication
from .utils import recover_to_addr, get_auth_eth_address
from .models import SignUp, SignUpStep
from .views import SignUpViewSet


class SignatureAuthMiddlewareTests(TestCase):
    # def test_signature_authentication_middleware(self):
    #     def inner(scope):
    #         expected = '0x6feb0cb327a812202f41ba50856ff985E4a781B5'.lower()
    #         self.assertEqual(scope['user'].username, expected)
    #         return True
    #     middleware = SignatureAuthMiddleware(inner=inner)
    #     self.assertIsNotNone(middleware.inner)
    #     sig = ''\
    #         '0x0b19d1d187c1145f08f4712241e2e24b011
    # b5eef6f1fe94f880fc1a8bf2e2' \
    #         '6513d16c7126dcce2fd4fa0f739ad566102657366cf2e1cde0164aed9b0e6b1'\
    #         '43921b'
    #     eth = '6feb0cb327a812202f41ba50856ff985E4a781B5'
    #     qs = 'auth_eth_address={}&auth_signature={}'.format(eth, sig)
    #     result = middleware({
    #         'query_string': bytes(qs, 'utf-8')
    #     })
    #     self.assertTrue(result)

    def test_mismatch_between_recovered(self):
        def inner(scope):
            self.assertIsInstance(scope['user'], AnonymousUser)
            return True
        middleware = SignatureAuthMiddleware(inner=inner)
        self.assertIsNotNone(middleware.inner)
        sig = ''\
            '0x0b19d1d187c1145f08f4712241e2e24b011b5eef6f1fe94f880fc1a8bf2e2' \
            '6513d16c7126dcce2fd4fa0f739ad566102657366cf2e1cde0164aed9b0e6b1'\
            '43921b'
        eth = '6feb0cb327a812202f41ba50856ff985E4a781B4'
        qs = 'auth_eth_address={}&auth_signature={}'.format(eth, sig)
        result = middleware({
            'query_string': bytes(qs, 'utf-8')
        })
        self.assertTrue(result)

    def test_signature_authentication_middleware_value_error(self):
        def inner(scope):
            self.assertIsInstance(scope['user'], AnonymousUser)
            return True
        middleware = SignatureAuthMiddleware(inner=inner)
        self.assertIsNotNone(middleware.inner)
        sig = 'some_wrong_signature_so_that_we_raise_value_error'
        eth = '6feb0cb327a812202f41ba50856ff985E4a781B5'
        qs = 'auth_eth_address={}&auth_signature={}'.format(eth, sig)
        result = middleware({
            'query_string': bytes(qs, 'utf-8')
        })
        self.assertTrue(result)

    def test_no_auth_parameters_provided(self):
        def inner(scope):
            self.assertIsInstance(scope['user'], AnonymousUser)
            return True
        middleware = SignatureAuthMiddleware(inner=inner)
        self.assertIsNotNone(middleware.inner)
        qs = ''
        result = middleware({
            'query_string': bytes(qs, 'utf-8')
        })
        self.assertTrue(result)


class AuthTests(TestCase):

    def test_signup(self):
        s = SignUp(email='test@example.com', step=SignUpStep.EMAIL)
        self.assertEqual(str(s), 'test@example.com')

    def test_recover_to_addr_string(self):
        sig = (
            '0xfbb93392ba8ec940b73b86cd66ae3df6674f73c0a0ec376cadd9a3133ea110'
            'f73935b8b89b51842c356ee27cfea6e1a583f7b55cd3e0d10106f2717355a395'
            '921b')
        addr = recover_to_addr('test', sig)
        self.assertEqual(addr, '0xc2d7cf95645d33006175b78989035c7c9061d3f9')

    def test_recover_to_addr_number(self):
        sig = (
            '0xb8d14178f867000541149445b0808b3b4707fe26c741d7d114786ab3546566'
            'cf315f0c4f94eb8b1cecd5eb24e0729a19711cbfc45b07eb6034a555e83bfd9e'
            'd31b')
        addr = recover_to_addr('12345', sig)
        self.assertEqual(addr, '0xc2d7cf95645d33006175b78989035c7c9061d3f9')

    def test_recover_to_addr_a0x_number(self):
        sig = (
            '0x410010ca0cf0adf3c78646eca1eb2562e48a223a9687d7e422d1700477dbb2'
            'ae7ec410a7a5ae6ca2f21bf231f8ab28f879b3616517d09028901fc425f86bbf'
            '131c')
        addr = recover_to_addr('a0x12345', sig)
        self.assertEqual(addr, '0xc2d7cf95645d33006175b78989035c7c9061d3f9')

    def test_recover_to_addr_value_error(self):
        class FakeRequest():
            META = {
                'HTTP_AUTH_SIGNATURE': 'some_sig_to_cause_value_error',
                'HTTP_AUTH_ETH_ADDRESS': '0xsomedefinitelywrongethaddress',
            }
        auth = SignatureAuthentication()
        result = auth.authenticate(FakeRequest)
        self.assertIsNone(result)

    def test_recover_to_addr_mismatch(self):
        sig = '' \
              '0x0b19d1d187c1145f08f4712241e2e24b011b5eef6f1fe94f880fc1a8bf' \
              '2e26513d16c7126dcce2fd4fa0f739ad566102657366cf2e1cde0164aed9' \
              'b0e6b143921b'

        class FakeRequest():
            META = {
                'HTTP_AUTH_SIGNATURE': sig,
                'HTTP_AUTH_ETH_ADDRESS': 'cb327a812202f41ba50856ff985E4a781B5',
            }
        auth = SignatureAuthentication()
        result = auth.authenticate(FakeRequest)
        self.assertIsNone(result)

    def test_get_auth_eth_address(self):
        eth_address = get_auth_eth_address({
            'HTTP_AUTH_ETH_ADDRESS': '0' * 40
        })
        self.assertEqual(eth_address, '0x{0}'.format('0' * 40))


class SignUpViewSetTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_create_of_signup_object(self):
        request = self.factory.post('/api/v1/signup/', data={
            'email': 'test@example.com'
        })
        response = SignUpViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)
        count = SignUp.objects.filter(email='test@example.com').count()
        self.assertEqual(count, 1)

    def test_create_of_signup_invalid_email(self):
        request = self.factory.post('/api/v1/signup/', data={
            'email': 'something_definitely_not_an_email'
        })
        response = SignUpViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)

    def test_create_of_not_unique_email(self):
        user, _ = User.objects.get_or_create(email='notunique@example.com')
        request = self.factory.post('/api/v1/signup/', data={
            'email': 'notunique@example.com'
        })
        response = SignUpViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 400)

    def test_create_user_email(self):
        eth_address = '0xD2BE64317Eb1832309DF8c8C18B09871809f3735'.lower()
        user, _ = User.objects.get_or_create(username=eth_address)
        request = self.factory.post(
            '/api/v1/signup/',
            data={
                'email': 'test@example.com'
            },
            HTTP_AUTH_SIGNATURE='0xe646de646dde9cee6875e3845428ce6fc13d41086e8a7f6531d1d526598cc4104122e01c38255d1e1d595710986d193f52e3dbc47cb01cb554d8e4572d6920361c',
            HTTP_AUTH_ETH_ADDRESS='D2BE64317Eb1832309DF8c8C18B09871809f3735'
        )
        response = SignUpViewSet.as_view({'post': 'create'})(request)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
