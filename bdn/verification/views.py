# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from bdn.auth.signature_authentication import SignatureAuthentication
from bdn.auth.utils import get_auth_eth_address
from .models import Verification
from .serializers import VerificationSerializer


class VerificationViewSet(viewsets.ModelViewSet):
    serializer_class = VerificationSerializer
    queryset = Verification.objects.none()

    def create(self, request):
        eth_address = get_auth_eth_address(request.META)
        data = request.data.copy()
        data['state'] = 'requested'
        serializer = VerificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data)
        else:
            response = Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response
