# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from bdn.auth.models import User
from bdn.certificate.models import Certificate
from bdn.auth.signature_authentication import SignatureAuthentication
from bdn.auth.utils import get_auth_eth_address
from .models import Verification
from .serializers import VerificationSerializer


class VerificationViewSet(viewsets.ModelViewSet):
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = VerificationSerializer
    queryset = Verification.objects.none()

    def create(self, request):
        eth_address = get_auth_eth_address(request.META)
        try:
            user = User.objects.get(username=eth_address)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        data = request.data.copy()
        data['state'] = 'requested'
        data['granted_to'] = user.id
        try:
            data['verifier'] = User.objects.get(
                username=str(request.data.get('verifier').lower())).id
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            data['certificate'] = Certificate.objects.get(
                id=request.data.get('id')).id
        except Certificate.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = VerificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data)
        else:
            response = Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response
