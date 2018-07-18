# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.http import JsonResponse

from django.forms.models import model_to_dict
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

    def create(self, request, pk=None):
        eth_address = '0x' + str(request.META.get('HTTP_AUTH_ETH_ADDRESS')).lower()
        profile_type = request.META.get('HTTP_PROFILE_TYPE')
        user = User.objects.get(username=eth_address)
        profile = Profile.objects.get(user=user)
        print(profile_type)
        if profile_type == '1':
            serializer = LearnerProfileSerializer(data=request.data, instance=profile, partial=True)
        elif profile_type == '2':
            serializer = AcademyProfileSerializer(data=request.data, instance=profile, partial=True)
        else:
            serializer = CompanyProfileSerializer(data=request.data, instance=profile, partial=True)
        if serializer.is_valid():
            print(serializer.validated_data)
            serializer.save()
            return Response({'status': 'ok'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

