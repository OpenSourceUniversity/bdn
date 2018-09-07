# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from bdn.auth.signature_authentication import SignatureAuthentication
from .models import Connections, FileUpload
from .serializers import ConnectionsSerializer, FileUploadSerializer
from bdn.auth.utils import get_auth_eth_address
from bdn.auth.models import User


class ConnectionsViewSet(viewsets.ModelViewSet):
    queryset = Connections.objects.all()
    serializer_class = ConnectionsSerializer
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk=None):
        return self.deny()

    def update(self, request):
        return self.deny()

    def partial_update(self, request):
        return self.deny()

    def destroy(self, request):
        return self.deny()

    @staticmethod
    def deny():
        return Response({
                    'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request):
        return Response({
                    'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)


class FileViewSet(viewsets.ModelViewSet):
    serializer_class = FileUploadSerializer
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, format=None):
        eth_address = get_auth_eth_address(request.META)
        try:
            user = User.objects.get(username=eth_address)
        except User.DoesNotExist:
            return Response({
                'error': 'User not found',
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            archive = serializer.save(
                owner=user,
                datafile=self.request.FILES['file']
            )
            return Response({
                'status': 'ok',
                'archive': archive.pk,
            })
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
