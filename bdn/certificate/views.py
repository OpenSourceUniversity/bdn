# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from bdn.auth.signature_authentication import SignatureAuthentication
from rest_framework.response import Response
from .models import Certificate
from bdn.course.models import Provider
from rest_framework.decorators import detail_route, list_route
from .serializers import CertificateSerializer
import datetime


class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        eth_address = '0x' + str(request.META.get('HTTP_AUTH_ETH_ADDRESS')).lower()
        certificates = Certificate.objects.filter(user_eth_address=eth_address)
        serializer = CertificateSerializer(certificates, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def get_certificates_count(self, request, pk=None):
        eth_address = request.GET.get('eth_address')
        certificates_count = len(Certificate.objects.filter(user_eth_address=eth_address))
        return Response({'certificates_count': certificates_count})

    @list_route(methods=['get'])
    def get_certificates_by_academy(self, request, pk=None):
        eth_address = '0x' + str(request.META.get('HTTP_AUTH_ETH_ADDRESS')).lower()
        certificates = Certificate.objects.filter(academy_address=eth_address)
        serializer = CertificateSerializer(certificates, many=True)
        return Response(serializer.data)

    def create(self, request, pk=None):
        eth_address = '0x' + str(request.META.get('HTTP_AUTH_ETH_ADDRESS')).lower()
        academy_address = str(request.data.get('academy_address')).lower()
        data = request.data.copy()
        date_format = '%Y-%m-%d'
        provider = None
        try:
            data['expiration_date'] = datetime.datetime.strptime(data['expiration_date'], date_format)
        except:
            print("Incorrect data format")
        try:
            provider = Provider.objects.get(eth_address=academy_address)
        except:
            print("Provider doesn't exist")
        serializer = CertificateSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user_eth_address=eth_address, academy_address=academy_address, provider=provider)
            return Response({'status': 'ok'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)