# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from bdn.auth.signature_authentication import SignatureAuthentication
from rest_framework.response import Response
from .models import Certificate
from bdn.course.models import Provider
from rest_framework.decorators import detail_route, list_route
from .serializers import CertificateSerializer, CertificateLearnerSerializer
import datetime


class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        eth_address = '0x{0}'.format(
            str(request.META.get('HTTP_AUTH_ETH_ADDRESS')).lower())
        certificates = Certificate.objects.filter(user_eth_address=eth_address)
        serializer = CertificateSerializer(certificates, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def get_certificates_count(self, request, pk=None):
        eth_address = request.GET.get('eth_address')
        certificates_count = len(
            Certificate.objects.filter(user_eth_address=eth_address))
        return Response({'certificates_count': certificates_count})

    @list_route(methods=['get'])
    def get_certificates_by_academy(self, request, pk=None):
        eth_address = '0x{0}'.format(
            str(request.META.get('HTTP_AUTH_ETH_ADDRESS')).lower())
        certificates = Certificate.objects.filter(
            academy_address=eth_address).order_by('verified', 'course_title')
        serializer = CertificateSerializer(certificates, many=True)
        return Response(serializer.data)

    @list_route(methods=['post'])
    def update_certificate_by_id(self, request, pk=None):
        eth_address = '0x{0}'.format(
            str(request.META.get('HTTP_AUTH_ETH_ADDRESS')).lower())
        certificate = Certificate.objects.get(id=request.data.get('id'))
        data = request.data.copy()
        date_format = '%Y-%m-%d'

        data['academy_address'] = certificate.academy_address
        data['learner_eth_address'] = certificate.learner_eth_address
        try:
            data['expiration_date'] = datetime.datetime.strptime(
                data['expiration_date'], date_format)
        except (ValueError, KeyError):
            data['expiration_date'] = None
        try:
            provider = Provider.objects.get(eth_address=eth_address)
        except Provider.DoesNotExist:
            provider = None

        if certificate.academy_address == eth_address:
            serializer = CertificateSerializer(
                data=data, instance=certificate, partial=True)
            if serializer.is_valid():
                serializer.save(provider=provider)
                return Response({'status': 'ok'})
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'denied'})

    @list_route(methods=['post'])
    def mass_verification(self, request, pk=None):
        eth_address = '0x{0}'.format(
            str(request.META.get('HTTP_AUTH_ETH_ADDRESS')).lower())
        ids = filter(lambda i: bool(i), request.data.get('ids').split('|'))
        certificates = Certificate.objects.filter(id__in=ids)
        for certificate in certificates:
            if certificate.academy_address == eth_address:
                certificate.verified = True
                certificate.save()
            else:
                return Response({'status': 'denied'})
        return Response({'status': 'ok'})

    @list_route(methods=['post'])
    def delete_by_id(self, request, pk=None):
        eth_address = '0x{0}'.format(
            str(request.META.get('HTTP_AUTH_ETH_ADDRESS')).lower())
        certificate = Certificate.objects.get(id=request.data.get('id'))
        if certificate.academy_address == eth_address:
            certificate.delete()
            return Response({'status': 'ok'})
        else:
            return Response({'status': 'denied'})

    def create(self, request, pk=None):
        eth_address = '0x{0}'.format(
            str(request.META.get('HTTP_AUTH_ETH_ADDRESS')).lower())
        academy_address = str(request.data.get('academy_address')).lower()
        data = request.data.copy()
        date_format = '%Y-%m-%d'

        try:
            data['expiration_date'] = datetime.datetime.strptime(
                data['expiration_date'], date_format)
        except (ValueError, KeyError):
            data['expiration_date'] = None
        try:
            provider = Provider.objects.get(eth_address=academy_address)
        except Provider.DoesNotExist:
            provider = None

        serializer = CertificateLearnerSerializer(data=data)
        if serializer.is_valid():
            serializer.save(
                user_eth_address=eth_address,
                academy_address=academy_address,
                provider=provider)
            return Response({'status': 'ok'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
