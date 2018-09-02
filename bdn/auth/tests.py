import unittest
from django.test import TestCase
from .signature_auth_middleware import SignatureAuthMiddleware
from .utils import recover_to_addr, get_auth_eth_address


class SignatureAuthMiddlewareTests(TestCase):
    def test_signature_authentication_middleware(self):
        def inner(scope):
            expected = '0x6feb0cb327a812202f41ba50856ff985E4a781B5'.lower()
            self.assertEqual(scope['user'].username, expected)
            return True
        middleware = SignatureAuthMiddleware(inner=inner)
        self.assertIsNotNone(middleware.inner)
        sig = ''\
            '0x0b19d1d187c1145f08f4712241e2e24b011b5eef6f1fe94f880fc1a8bf2e2' \
            '6513d16c7126dcce2fd4fa0f739ad566102657366cf2e1cde0164aed9b0e6b1'\
            '43921b'
        eth = '6feb0cb327a812202f41ba50856ff985E4a781B5'
        qs = 'auth_eth_address={}&auth_signature={}'.format(eth, sig)
        result = middleware({
            'query_string': bytes(qs, 'utf-8')
        })
        self.assertTrue(result)


class AuthTests(TestCase):

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

    def test_get_auth_eth_address(self):
        eth_address = get_auth_eth_address({
            'HTTP_AUTH_ETH_ADDRESS': '0' * 40
        })
        self.assertEqual(eth_address, '0x{0}'.format('0' * 40))


if __name__ == '__main__':
    unittest.main()
