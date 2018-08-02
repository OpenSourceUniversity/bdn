# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from bdn.auth.signature_authentication import SignatureAuthentication
from rest_framework.response import Response
from .models import Certificate
from bdn.auth.utils import get_auth_eth_address
from bdn.course.models import Provider
from rest_framework.decorators import detail_route, list_route
from .serializers import CertificateSerializer, CertificateLearnerSerializer
import datetime


class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk=None):
        eth_address = get_auth_eth_address(request.META)
        certificate = Certificate.objects.get(id=pk)
        if (certificate.academy_address == eth_address or certificate.learner_eth_address == eth_address):
            serializer = CertificateSerializer(certificate)
            return Response(serializer.data)
        return Response({
                    'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request):
        return Response({
                    'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)

    def partial_update(self, request):
        return Response({
                    'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request):
        return Response({
                    'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)

    def list(self, request):
        eth_address = get_auth_eth_address(request.META)
        certificates = Certificate.objects.filter(user_eth_address=eth_address)
        serializer = CertificateSerializer(certificates, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def get_certificates_count(self, request, pk=None):
        # TODO: instead of passing over unused pk, pass over the ETH address
        # instead of getting it through the GET parameters
        eth_address = pk.lower()
        certificates_count = Certificate.objects.filter(
            user_eth_address=eth_address).count()
        return Response({'certificates_count': certificates_count})

    @list_route(methods=['get'])
    def get_certificates_by_academy(self, request):
        eth_address = get_auth_eth_address(request.META)
        certificates = Certificate.objects.filter(
            academy_address=eth_address).order_by('verified', 'course_title')
        serializer = CertificateSerializer(certificates, many=True)
        return Response(serializer.data)

    @list_route(methods=['post'])
    def update_certificate_by_id(self, request):
        eth_address = get_auth_eth_address(request.META)
        certificate = Certificate.objects.get(id=request.data.get('id'))
        data = request.data.copy()
        date_format = '%Y-%m-%d'

        data['academy_address'] = certificate.academy_address
        data['learner_eth_address'] = certificate.learner_eth_address
        try:
            data['expiration_date'] = datetime.datetime.strptime(
                data['expiration_date'], date_format)
        except (ValueError, KeyError, TypeError):
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
            return Response({
                'status': 'denied'
            }, status=status.HTTP_401_UNAUTHORIZED)

    @list_route(methods=['post'])
    def mass_verification(self, request):
        eth_address = get_auth_eth_address(request.META)
        ids = filter(lambda i: bool(i), request.data.get('ids').split('|'))
        certificates = Certificate.objects.filter(id__in=ids)
        for certificate in certificates:
            if certificate.academy_address == eth_address:
                certificate.verified = True
                certificate.save()
            else:
                return Response({
                    'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'status': 'ok'})

    @list_route(methods=['post'])
    def delete_by_id(self, request):
        eth_address = get_auth_eth_address(request.META)
        certificate = Certificate.objects.get(id=str(request.data.get('id')))
        if certificate.academy_address == eth_address:
            certificate.delete()
            return Response({'status': 'ok'})
        else:
            return Response({
                'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, pk=None):
        eth_address = get_auth_eth_address(request.META)
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
