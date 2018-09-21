# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from bdn.auth.signature_authentication import SignatureAuthentication
from .serializers import FileUploadSerializer
from .tasks import import_connections


class FileViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = FileUploadSerializer
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        file_upload = serializer.save()
        import_connections.delay(file_upload.id)

    def get_serializer(self, data, *args, **kwargs):
        data['owner'] = self.request.user.id
        return super().get_serializer(data=data, *args, **kwargs)
