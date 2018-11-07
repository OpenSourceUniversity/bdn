# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from bdn.utils.send_email_tasks import certificate_upload_email
from bdn.auth.signature_authentication import SignatureAuthentication
from bdn.auth.utils import get_auth_eth_address
from bdn.auth.models import User
from bdn.skill.models import Skill
from bdn.industry.models import Industry
from bdn.verification.models import Verification
from .models import Certificate
from .serializers import (CertificateSerializer,
                          CertificateViewProfileSerializer)


class CertificateViewSet(mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateViewProfileSerializer
    authentication_classes = (SignatureAuthentication,)

    def get_permissions(self):
        if self.action and (
                self.action in ('retrieve', 'get_certificates_by_learner')):
            self.permission_classes = [IsAuthenticatedOrReadOnly, ]
        else:
            self.permission_classes = [IsAuthenticated, ]
        return super(self.__class__, self).get_permissions()

    def retrieve(self, request, pk=None):
        certificate = Certificate.objects.get(id=pk)
        serializer = CertificateViewProfileSerializer(
            certificate, context={'request': request})
        return Response(serializer.data)

    @staticmethod
    def deny():
        return Response({
                    'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)

    def list(self, request):
        certificates = Certificate.objects\
            .filter(holder=request.user, granted_to_type=1)\
            .order_by('certificate_title')
        serializer = CertificateViewProfileSerializer(certificates, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def get_certificates_by_learner(self, request):
        eth_address = str(request.GET.get('eth_address')).lower()
        certificates = Certificate.objects\
            .filter(holder__username__iexact=eth_address, granted_to_type=1)\
            .order_by('certificate_title')
        serializer = CertificateViewProfileSerializer(certificates, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def delete_by_id(self, request, pk=None):
        certificate = Certificate.objects.get(id=str(pk))
        if certificate.holder == request.user:
            certificate.delete()
            return Response({'status': 'ok'})
        return self.deny()

    def create(self, request):
        eth_address = get_auth_eth_address(request.META)
        academy_address = str(request.data.get('academy_address')).lower()
        industries = Industry.objects.filter(
            name__in=request.data.get('industries', []))
        data = request.data.copy()
        expiration_date = self._normalized_date(data.get('expiration_date'))
        data['expiration_date'] = expiration_date
        holder_eth_address = request.data.get('holder_eth_address').lower()
        try:
            holder = User.objects.get(username=holder_eth_address)
        except User.DoesNotExist:
            return Response({
                'error': 'User not found',
            }, status=status.HTTP_400_BAD_REQUEST)
        skills = self._normalized_skills(request.data.get('skills', []))
        data['holder'] = holder.id
        data['academy_address'] = academy_address
        data['user_eth_address'] = eth_address
        serializer = CertificateSerializer(data=data)
        if serializer.is_valid():
            certificate = serializer.save(
                skills=skills, industries=industries)
            issuer_type = request.user.profile.active_profile_type
            if (issuer_type != 1 and
               holder.username != request.user.username):
                verification = Verification(
                    certificate=certificate, granted_to=holder,
                    verifier=request.user, verifier_type=issuer_type,
                    granted_to_type=int(data['granted_to_type']))
                verification.save()
                if holder.usersettings.subscribed:
                    certificate_upload_email.delay(
                        certificate.certificate_title,
                        request.user.profile.name_by_profile_type(
                            issuer_type),
                        holder.email
                        )
            elif holder.usersettings.subscribed:
                certificate_upload_email.delay(
                    certificate.certificate_title,
                    holder.profile.name_by_profile_type(
                        issuer_type),
                    holder.email
                    )
            return Response({
                'status': 'ok',
                'certificate_pk': certificate.pk,
            })
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def _normalized_skills(skill_names):
        skills = []
        for skill_name in skill_names:
            try:
                skill_obj = Skill.objects.get(name=skill_name.strip())
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
