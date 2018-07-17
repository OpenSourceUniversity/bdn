# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
from django.http import JsonResponse, HttpResponse
from django.views import View

from django.forms.models import model_to_dict
from django.shortcuts import render
from rest_framework import viewsets, mixins, status
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from bdn.auth.signature_authentication import SignatureAuthentication
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer

# Create your views here.
def update_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    user.profile.learner_position = 'Lorem ipsum dolor sit'
    user.save()


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)


class ProfileView(View):
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    def get(self, request):
        eth_address = '0x' + str(request.META.get('HTTP_AUTH_ETH_ADDRESS')).lower()
        user = User.objects.get(username=eth_address)
        profile = Profile.objects.get(user=user)
        serializer = self.serializer_class(data=model_to_dict(profile))
        serializer.is_valid(raise_exception=True)
        response = JsonResponse(json.dumps(serializer.data), safe=False)
        return response
