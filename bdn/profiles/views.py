# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status, viewsets
from rest_framework.decorators import detail_route, list_route
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from bdn.auth.signature_authentication import SignatureAuthentication
from rest_framework.response import Response
from bdn.auth.utils import get_auth_eth_address
from .models import Profile, ProfileType
from bdn.course.models import Course
from bdn.provider.models import Provider
from bdn.certificate.models import Certificate
from bdn.job.models import Job
from bdn.company.models import Company
from bdn.provider.serializers import ProviderSerializer
from bdn.company.serializers import CompanySerializer
from .serializers import (
    ProfileSerializer, LearnerProfileSerializer, AcademyProfileSerializer,
    CompanyProfileSerializer)


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()

    def retrieve(self, request):
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
        user = User.objects.get(username=eth_address)
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def get_academy(self, request, pk=None):
        eth_address = pk.lower()
        try:
            user = User.objects.get(username=eth_address)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        profile = Profile.objects.get(user=user)
        serializer = AcademyProfileSerializer(profile)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def get_learner(self, request, pk=None):
        eth_address = pk.lower()
        try:
            user = User.objects.get(username=eth_address)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        profile = Profile.objects.get(user=user)
        if profile.public_profile:
            serializer = LearnerProfileSerializer(profile)
            return Response(serializer.data)
        else:
            return Response({'is_public': False})

    @detail_route(methods=['get'])
    def get_business(self, request, pk=None):
        eth_address = pk.lower()
        try:
            user = User.objects.get(username=eth_address)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        profile = Profile.objects.get(user=user)
        serializer = CompanyProfileSerializer(profile)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def get_academies(self, request):
        providers_obj = Provider.objects.all()
        eth_addresses = set()
        for obj in providers_obj:
            eth_addresses.add(obj.eth_address)
        users = User.objects.filter(username__in=eth_addresses)
        profiles = Profile.objects\
            .filter(user__in=users).order_by('academy_name')
        serializer = AcademyProfileSerializer(profiles, many=True)
        newdata = []
        for data in serializer.data:
            provider = Provider.objects.get(
                eth_address=data.get('user').get('username'))
            courses_count = Course.objects.all().filter(
                provider=provider).count()
            data['courses_count'] = courses_count
            newdata.append(data)
        return Response(newdata)

    @list_route(methods=['get'])
    def get_businesses(self, request):
        companies_obj = Company.objects.all()
        eth_addresses = set()
        for obj in companies_obj:
            eth_addresses.add(obj.eth_address)
        users = User.objects.filter(username__in=eth_addresses)
        profiles = Profile.objects\
            .filter(user__in=users)\
            .order_by('company_name')
        serializer = CompanyProfileSerializer(profiles, many=True)
        newdata = []
        for data in serializer.data:
            company = Company.objects.get(
                eth_address=data.get('user').get('username'))
            jobs_count = Job.objects.all().filter(company=company).count()
            data['jobs_count'] = jobs_count
            newdata.append(data)
        return Response(newdata)

    @list_route(methods=['get'])
    def get_learners(self, request):
        profiles = Profile.objects.filter(
            public_profile=True).order_by('first_name')
        serializer = LearnerProfileSerializer(profiles, many=True)
        newdata = []
        for data in serializer.data:
            certificates_count = Certificate.objects.all().filter(
                learner_eth_address=data.get('user').get('username')).count()
            data['certificates_count'] = certificates_count
            newdata.append(data)
        return Response(newdata)

    def create(self, request, pk=None):
        eth_address = get_auth_eth_address(request.META)
        profile_type = int(request.META.get('HTTP_PROFILE_TYPE'))
        user = User.objects.get(username=eth_address)
        profile = Profile.objects.get(user=user)
        data = request.data.copy()
        if profile_type == ProfileType.LEARNER:
            if data['learner_avatar'] is None:
                data['learner_avatar'] = profile.learner_avatar
            serializer = LearnerProfileSerializer(
                data=data, instance=profile, partial=True)
        elif profile_type == ProfileType.ACADEMY:
            if data['academy_logo'] is None:
                data['academy_logo'] = profile.academy_logo
            serializer = AcademyProfileSerializer(
                data=data, instance=profile, partial=True)
            provider, created = Provider.objects.get_or_create(
                    eth_address=eth_address)
            if created:
                provider_serializer = ProviderSerializer(
                    data={'name': request.data.get('academy_name')},
                    instance=provider, partial=True)
                if provider_serializer.is_valid():
                    provider_serializer.save()
                else:
                    return Response(provider_serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                provider_serializer = ProviderSerializer(
                    data={'name': request.data.get('academy_name')},
                    instance=provider, partial=True)
                if provider_serializer.is_valid():
                    provider_serializer.save()
                else:
                    return Response(provider_serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)
        elif profile_type == ProfileType.BUSINESS:
            if data['company_logo'] is None:
                    data['company_logo'] = profile.company_logo
            serializer = CompanyProfileSerializer(
                data=data, instance=profile, partial=True)
            company, created = Company.objects.get_or_create(
                    eth_address=eth_address)
            if created:
                company_serializer = CompanySerializer(
                    data={'name': request.data.get('company_name')},
                    instance=company, partial=True)
                if company_serializer.is_valid():
                    company_serializer.save()
                else:
                    return Response(company_serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
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
