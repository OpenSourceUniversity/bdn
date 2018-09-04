from django.test import TestCase
from .serializers import CompanySerializer


class CompanyTests(TestCase):
    def test_company_eth_address(self):
        class FakeCompany:
            class user:
                username = '0x0'
        serializer = CompanySerializer()
        result = serializer._eth_address(FakeCompany)
        self.assertEqual(result, '0x0')
