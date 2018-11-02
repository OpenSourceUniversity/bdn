# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models import Q
from haystack.query import SearchQuerySet
from rest_framework.response import Response
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import detail_route, list_route
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.pagination import LimitOffsetPagination
from bdn.auth.signature_authentication import SignatureAuthentication
from .models import Profile, ProfileType
from bdn.provider.models import Provider
from bdn.company.models import Company
from bdn.provider.serializers import ProviderSerializer
from bdn.company.serializers import CompanySerializer
from .utils import get_profile_by_type
from .serializers import (
    ProfileSerializer, LearnerProfileSerializer, AcademyProfileSerializer,
    CompanyProfileSerializer, LearnerViewProfileSerializer)


class ProfileViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = ProfileSerializer
    pagination_class = LimitOffsetPagination
    authentication_classes = (SignatureAuthentication,)
    queryset = Profile.objects.all()

    def get_permissions(self):
        if self.action and (self.action in (
                'get_academy', 'get_learner', 'get_business')):
            self.permission_classes = [IsAuthenticatedOrReadOnly, ]
        else:
            self.permission_classes = [IsAuthenticated, ]
        return super(self.__class__, self).get_permissions()

    def list(self, request):
        user = request.user
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def get_academy(self, request, pk=None):
        return get_profile_by_type(pk, ProfileType.ACADEMY)

    @detail_route(methods=['get'])
    def get_learner(self, request, pk=None):
        eth_address = pk.lower()
        profile = Profile.objects.get(user__username__iexact=eth_address)
        if not profile.public_profile:
            return Response({
                'is_public': False
            }, status=status.HTTP_403_FORBIDDEN)
        serializer = LearnerViewProfileSerializer(profile)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def get_business(self, request, pk=None):
        return get_profile_by_type(pk, ProfileType.BUSINESS)

    @list_route(methods=['get'])
    def get_academies(self, request):
        return self._get_profiles_by_type(
            request,
            AcademyProfileSerializer,
            Q(user__provider__isnull=False),
            'academy_name')

    @list_route(methods=['get'])
    def get_businesses(self, request):
        return self._get_profiles_by_type(
            request,
            CompanyProfileSerializer,
            Q(user__company__isnull=False),
            'company_name')

    @list_route(methods=['get'])
    def get_learners(self, request):
        return self._get_profiles_by_type(
            request,
            LearnerViewProfileSerializer,
            Q(public_profile=True, full_name__isnull=False),
            'full_name')

    def _get_profiles_by_type(
            self, request, serializer_cls, filter_query, name_field):

        search_query = self.request.GET.get('q')
        if search_query:
            sqs = SearchQuerySet().filter(**{name_field: search_query})\
                .models(Profile)
            profiles = [result.object for result in sqs if result.object]
        else:
            profiles = Profile.objects.filter(filter_query)\
                .order_by(name_field)

        page = self.paginate_queryset(profiles)
        if page is not None:
            serializer = serializer_cls(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializer_cls(profiles, many=True)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def autocomplete(self, request):
        AUTOCOMPLETE_SIZE = 10
        query = request.GET.get('q', '')
        name_field = request.GET.get('name_field', 'full_name')
        sqs = SearchQuerySet()\
            .filter(**{'{}_auto'.format(name_field): query})\
            .models(Profile)
        result = []
        result_set = set()
        for r in sqs:
            if AUTOCOMPLETE_SIZE == len(result_set):
                break
            if r.object:
                name = getattr(r.object, name_field)
                if name not in result_set:
                    result.append(name)
                    result_set.add(name)
        return Response(result, status=status.HTTP_200_OK)

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
        else:
            return Response({'error': 'Wrong active profile type'},
                            status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'ok'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
