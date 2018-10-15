# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import zipfile
import codecs
import csv
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from bdn.auth.signature_authentication import SignatureAuthentication
from rest_framework.response import Response
from .tasks import handle_connection_row


class FileViewSet(viewsets.GenericViewSet):
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, format=None):
        file_upload = request.FILES['datafile']
        with zipfile.ZipFile(file_upload) as connection_zip:
            with connection_zip.\
                    open('Connections.csv', 'r') as connection_file:
                connection_file = codecs.iterdecode(connection_file, 'utf-8')
                reader = csv.reader(
                    connection_file, delimiter=',', quotechar='"')
                for index, row in enumerate(reader):
                    # Skip the header
                    if index == 0:
                        continue
                    handle_connection_row.delay(str(request.user.id), row)
        return Response({'status': 'ok'})
