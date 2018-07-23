# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status, viewsets
from rest_framework.decorators import detail_route
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from bdn.auth.signature_authentication import SignatureAuthentication
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer, LearnerProfileSerializer, AcademyProfileSerializer, CompanyProfileSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()

    def list(self, request):
        eth_address = '0x' + str(request.META.get('HTTP_AUTH_ETH_ADDRESS')).lower()
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
        serializer = LearnerProfileSerializer(profile)
        return Response(serializer.data)

    @detail_route(methods=['get'])
    def get_business(self, request, pk=None):
        eth_address = request.GET.get('eth_address')
        user = User.objects.get(username=eth_address)
        profile = Profile.objects.get(user=user)
        serializer = CompanyProfileSerializer(profile)
        return Response(serializer.data)


    def create(self, request, pk=None):
        eth_address = '0x' + str(request.META.get('HTTP_AUTH_ETH_ADDRESS')).lower()
        profile_type = request.META.get('HTTP_PROFILE_TYPE')
        user = User.objects.get(username=eth_address)
        profile = Profile.objects.get(user=user)
        if profile_type == '1':
            serializer = LearnerProfileSerializer(data=request.data, instance=profile, partial=True)
        elif profile_type == '2':
            serializer = AcademyProfileSerializer(data=request.data, instance=profile, partial=True)
        elif profile_type == '3':
            serializer = CompanyProfileSerializer(data=request.data, instance=profile, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'ok'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

