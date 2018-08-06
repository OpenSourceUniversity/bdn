# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from bdn.auth.signature_authentication import SignatureAuthentication
from rest_framework.response import Response
from .models import Certificate
from bdn.auth.utils import get_auth_eth_address
from bdn.course.models import Provider, Skill, Category
from rest_framework.decorators import detail_route, list_route
from .serializers import (CertificateSerializer, CertificateLearnerSerializer,
                          CertificateViewProfileSerializer)
import datetime


class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk=None):
        eth_address = get_auth_eth_address(request.META)
        certificate = Certificate.objects.get(id=pk)
        if (certificate.academy_address == eth_address or
                certificate.learner_eth_address == eth_address):
            serializer = CertificateSerializer(certificate)
            return Response(serializer.data)
        return self.deny()

    def update(self, request):
        return self.deny()

    def partial_update(self, request):
        return self.deny()

    def destroy(self, request):
        return self.deny()

    @staticmethod
    def deny():
        return Response({
                    'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)

    def list(self, request):
        eth_address = get_auth_eth_address(request.META)
        certificates = Certificate.objects\
            .filter(learner_eth_address=eth_address)\
            .order_by('-verified', 'course_title')
        serializer = CertificateSerializer(certificates, many=True)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def get_certificates_count(self, request, pk=None):
        eth_address = pk.lower()
        certificates_count = Certificate.objects.filter(
            learner_eth_address=eth_address).count()
        return Response({'certificates_count': certificates_count})

    @list_route(methods=['get'])
    def get_certificates_by_academy(self, request):
        eth_address = get_auth_eth_address(request.META)
        certificates = Certificate.objects.filter(
            academy_address=eth_address).order_by('verified', 'course_title')
        serializer = CertificateSerializer(certificates, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def get_certificates_by_learner(self, request):
        eth_address = str(request.GET.get('eth_address')).lower()
        certificates = Certificate.objects\
            .filter(learner_eth_address=eth_address)\
            .order_by('-verified', 'course_title')
        serializer = CertificateViewProfileSerializer(certificates, many=True)
        return Response(serializer.data)

    @list_route(methods=['post'])
    def update_certificate_by_id(self, request):
        eth_address = get_auth_eth_address(request.META)
        certificate = Certificate.objects.get(id=request.data.get('id'))
        data = request.data.copy()
        categories = Category.objects.filter(
            name__in=request.data.get('categories'))
        data['academy_address'] = certificate.academy_address
        data['learner_eth_address'] = certificate.learner_eth_address
        data['ipfs_hash'] = certificate.ipfs_hash
        data['user_eth_address'] = certificate.user_eth_address
        data['skills'] = self._normalized_skills(request.data.get('skills'))
        data['categories'] = categories
        expiration_date = self._normalized_date(data['expiration_date'])
        data['expiration_date'] = expiration_date
        provider = Provider.objects.filter(eth_address=eth_address).first()

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
            return self.deny()

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
                return self.deny()
        return Response({'status': 'ok'})

    @list_route(methods=['post'])
    def delete_by_id(self, request):
        eth_address = get_auth_eth_address(request.META)
        certificate = Certificate.objects.get(id=str(request.data.get('id')))
        if certificate.academy_address == eth_address:
            certificate.delete()
            return Response({'status': 'ok'})
        else:
            return self.deny()

    def create(self, request, pk=None):
        eth_address = get_auth_eth_address(request.META)
        academy_address = str(request.data.get('academy_address')).lower()
        categories = Category.objects.filter(
            name__in=request.data.get('categories'))
        data = request.data.copy()
        expiration_date = self._normalized_date(data['expiration_date'])
        data['expiration_date'] = expiration_date
        provider = Provider.objects.filter(eth_address=academy_address).first()
        learner_eth_address = request.data.get('learner_eth_address').lower()

        skills = self._normalized_skills(request.data.get('skills'))
        data['learner_eth_address'] = learner_eth_address
        data['academy_address'] = academy_address
        data['user_eth_address'] = eth_address
        serializer = CertificateLearnerSerializer(data=data)
        if serializer.is_valid():
            serializer.save(
                provider=provider, skills=skills, categories=categories)
            return Response({'status': 'ok'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def _normalized_skills(skill_names):
        skills = []
        for skill_name in skill_names:
            try:
                skill_obj = Skill.objects.get(name__iexact=skill_name.strip())
            except Skill.DoesNotExist:
                skill_obj = Skill(name=skill_name, standardized=False)
                skill_obj.save()
            skills.append(skill_obj)
        return skills

    @staticmethod
    def _normalized_date(date):
        DATE_FORMAT = '%Y-%m-%d'
        try:
            return datetime.datetime.strptime(date, DATE_FORMAT)
        except (ValueError, KeyError, TypeError):
            pass
