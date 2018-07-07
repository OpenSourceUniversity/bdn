import unittest
from django.test import TestCase
from .utils import recover_to_addr


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

    def test_recover_to_addr_0x_number(self):
        sig = (
            '0x2d1693bb4c335caa2ecfca2a76c192a5158e15369bf83190624a33033ae30f'
            'f90cf02ee869846d245fe09c2e121d2c6691ab161ecd4ee9c14f201593a5836d'
            '231c')
        addr = recover_to_addr('0x12345', sig)
        self.assertEqual(addr, '0xc2d7cf95645d33006175b78989035c7c9061d3f9')

    def test_recover_to_addr_a0x_number(self):
        sig = (
            '0x410010ca0cf0adf3c78646eca1eb2562e48a223a9687d7e422d1700477dbb2'
            'ae7ec410a7a5ae6ca2f21bf231f8ab28f879b3616517d09028901fc425f86bbf'
            '131c')
        addr = recover_to_addr('a0x12345', sig)
        self.assertEqual(addr, '0xc2d7cf95645d33006175b78989035c7c9061d3f9')


if __name__ == '__main__':
    unittest.main()
