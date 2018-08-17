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
        data = request.data.copy()
        eth_address = get_auth_eth_address(request.META)
        try:
            granted_to = User.objects.get(username__iexact=eth_address)
            verifier = User.objects.get(username__iexact=data['verifier'])
        except User.DoesNotExist:
            return Response({
                'error': 'User not found',
            }, status=status.HTTP_400_BAD_REQUEST)

        data['state'] = 'requested'
        data['granted_to'] = granted_to.id
        data['verifier'] = verifier.id

        duplicate_verification = Verification.objects.filter(
            granted_to=granted_to,
            verifier=verifier, certificate__id=data['certificate']).first()
        if duplicate_verification:
            return Response({
                'error': 'Duplicate verification request found',
                'id': duplicate_verification.id,
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = VerificationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data)
        else:
            response = Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response
