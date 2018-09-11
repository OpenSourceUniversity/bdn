# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status, viewsets, mixins
from rest_framework.decorators import detail_route, list_route
from bdn.auth.models import User
from rest_framework.permissions import IsAuthenticated
from bdn.auth.signature_authentication import SignatureAuthentication
from rest_framework.response import Response
from .models import Profile, ProfileType
from bdn.provider.models import Provider
from bdn.company.models import Company
from bdn.provider.serializers import ProviderSerializer
from bdn.company.serializers import CompanySerializer
from .serializers import (
    ProfileSerializer, LearnerProfileSerializer, AcademyProfileSerializer,
    CompanyProfileSerializer)


class ProfileViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = ProfileSerializer
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()

    def list(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    @staticmethod
    def _get_profile_by_type(pk, profile_type):
        SERIALIZERS = {
            ProfileType.ACADEMY: AcademyProfileSerializer,
            ProfileType.BUSINESS: CompanyProfileSerializer,
            ProfileType.LEARNER: LearnerProfileSerializer,
        }
        serializer_cls = SERIALIZERS[profile_type]
        eth_address = pk.lower()
        try:
            profile = Profile.objects.get(user__username__iexact=eth_address)
            serializer = serializer_cls(profile)
            response = Response(serializer.data)
        except User.DoesNotExist:
            response = Response(status=status.HTTP_400_BAD_REQUEST)
        return response

    @detail_route(methods=['get'])
    def get_academy(self, request, pk=None):
        return self._get_profile_by_type(pk, ProfileType.ACADEMY)

    @detail_route(methods=['get'])
    def get_learner(self, request, pk=None):
        eth_address = pk.lower()
        profile = Profile.objects.get(user__username__iexact=eth_address)
        if not profile.public_profile:
            return Response({
                'is_public': False
            }, status=status.HTTP_403_FORBIDDEN)
        return self._get_profile_by_type(pk, ProfileType.LEARNER)

    @detail_route(methods=['get'])
    def get_business(self, request, pk=None):
        return self._get_profile_by_type(pk, ProfileType.BUSINESS)

    @list_route(methods=['get'])
    def get_academies(self, request):
        profiles = Profile.objects\
            .filter(user__provider__isnull=False)\
            .order_by('academy_name')
        serializer = AcademyProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def get_businesses(self, request):
        profiles = Profile.objects\
            .filter(user__company__isnull=False)\
            .order_by('company_name')
        serializer = CompanyProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def get_learners(self, request):
        profiles = Profile.objects.filter(
            public_profile=True).order_by('first_name')
        serializer = LearnerProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    @list_route(methods=['post'])
    def set_active_profile(self, request):
        profile = request.user.profile
        profile_type = int(request.META.get('HTTP_PROFILE_TYPE'))
        profile.active_profile_type = profile_type
        profile.save()
        return Response({'status': 'ok'})

    @list_route(methods=['get'])
    def get_active_profile(self, request):
        profile = request.user.profile
        return Response({
                'active_profile_type': profile.active_profile_type
            })

    def create(self, request, pk=None):
        profile_type = int(request.META.get('HTTP_PROFILE_TYPE'))
        profile = request.user.profile
        data = request.data.copy()
        if profile_type == ProfileType.LEARNER:
            learner_avatar = data.get('learner_avatar')
            if learner_avatar is None:
                data['learner_avatar'] = profile.learner_avatar
            serializer = LearnerProfileSerializer(
                data=data, instance=profile, partial=True)
        elif profile_type == ProfileType.ACADEMY:
            academy_logo = data.get('academy_logo')
            if academy_logo is None:
                data['academy_logo'] = profile.academy_logo
            serializer = AcademyProfileSerializer(
                data=data, instance=profile, partial=True)
            provider, _ = Provider.objects.get_or_create(
                    user=request.user)
            provider_serializer = ProviderSerializer(
                data={'name': request.data.get('academy_name')},
                instance=provider, partial=True)
            if provider_serializer.is_valid():
                provider_serializer.save()
            else:
                return Response(provider_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        elif profile_type == ProfileType.BUSINESS:
            company_logo = data.get('company_logo')
            if company_logo is None:
                    data['company_logo'] = profile.company_logo
            serializer = CompanyProfileSerializer(
                data=data, instance=profile, partial=True)
            company, _ = Company.objects.get_or_create(
                    user=request.user)
            company_serializer = CompanySerializer(
                data={'name': request.data.get('company_name')},
                instance=company, partial=True)
            if company_serializer.is_valid():
                company_serializer.save()
            else:
                return Response(company_serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'ok'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
