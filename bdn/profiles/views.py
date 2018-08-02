# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status, viewsets
from rest_framework.decorators import detail_route, list_route
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from bdn.auth.signature_authentication import SignatureAuthentication
from rest_framework.response import Response
from .models import Profile
from bdn.course.models import Provider, Course
from bdn.job.models import Company, Job
from bdn.course.serializers import ProviderSerializer
from bdn.job.serializers import CompanySerializer
from .serializers import (
    ProfileSerializer, LearnerProfileSerializer, AcademyProfileSerializer,
    CompanyProfileSerializer)


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()

    def list(self, request):
        eth_address = '0x' + str(request.META.get(
            'HTTP_AUTH_ETH_ADDRESS')).lower()
        user = User.objects.get(username=eth_address)
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def get_academy(self, request, pk=None):
        eth_address = request.GET.get('eth_address')
        user = User.objects.get(username=eth_address)
        profile = Profile.objects.get(user=user)
        serializer = AcademyProfileSerializer(profile)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def get_learner(self, request, pk=None):
        eth_address = request.GET.get('eth_address')
        user = User.objects.get(username=eth_address)
        profile = Profile.objects.get(user=user)
        if profile.public_profile:
            serializer = LearnerProfileSerializer(profile)
            return Response(serializer.data)
        else:
            return Response({'is_public': False})

    @detail_route(methods=['get'])
    def get_business(self, request, pk=None):
        eth_address = request.GET.get('eth_address')
        user = User.objects.get(username=eth_address)
        profile = Profile.objects.get(user=user)
        serializer = CompanyProfileSerializer(profile)
        return Response(serializer.data)

    @list_route(methods=['get'])
    def get_academies(self, request, pk=None):
        providers_obj = Provider.objects.all()
        eth_addresses = set()
        for obj in providers_obj:
            eth_addresses.add(obj.eth_address)
        users = User.objects.filter(username__in=eth_addresses)
        profiles = Profile.objects.filter(user__in=users)
        serializer = AcademyProfileSerializer(profiles, many=True)
        newdata = []
        for data in serializer.data:
            provider = Provider.objects.get(
                eth_address=data.get('user').get('username'))
            courses_count = len(Course.objects.all().filter(
                provider=provider))
            data['courses_count'] = courses_count
            newdata.append(data)
        return Response(newdata)

    @list_route(methods=['get'])
    def get_businesses(self, request, pk=None):
        companies_obj = Company.objects.all()
        eth_addresses = set()
        for obj in companies_obj:
            eth_addresses.add(obj.eth_address)
        users = User.objects.filter(username__in=eth_addresses)
        profiles = Profile.objects.filter(user__in=users)
        serializer = CompanyProfileSerializer(profiles, many=True)
        newdata = []
        for data in serializer.data:
            company = Company.objects.get(
                eth_address=data.get('user').get('username'))
            jobs_count = len(Job.objects.all().filter(company=company))
            data['jobs_count'] = jobs_count
            newdata.append(data)
        return Response(newdata)

    def create(self, request, pk=None):
        eth_address = '0x' + str(request.META.get(
            'HTTP_AUTH_ETH_ADDRESS')).lower()
        profile_type = request.META.get('HTTP_PROFILE_TYPE')
        user = User.objects.get(username=eth_address)
        profile = Profile.objects.get(user=user)
        if profile_type == '1':
            serializer = LearnerProfileSerializer(
                data=request.data, instance=profile, partial=True)
        elif profile_type == '2':
            serializer = AcademyProfileSerializer(
                data=request.data, instance=profile, partial=True)
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
        elif profile_type == '3':
            serializer = CompanyProfileSerializer(
                data=request.data, instance=profile, partial=True)
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
