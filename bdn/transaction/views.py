# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict
from rest_framework import viewsets, status, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from bdn.auth.signature_authentication import SignatureAuthentication
from .models import Transaction
from .serializers import TransactionSerializer


class TransactionPagination(LimitOffsetPagination):
    default_limit = 30
    max_limit = 30

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class TransactionViewSet(mixins.CreateModelMixin,
                         mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TransactionSerializer
    pagination_class = TransactionPagination

    @staticmethod
    def deny():
        return Response({
                    'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)

    def get_queryset(self):
        username = self.request.user.username
        transactions = Transaction.objects.filter(
            sender=username).\
            order_by('-date')
        return transactions

    def create(self, request):
        sender = request.user.username
        data = request.data.copy()
        data['sender'] = sender
        data['receiver'] = data['receiver'].lower()
        print(data)
        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            transaction = serializer.save()
            response = Response(TransactionSerializer(transaction).data)
        else:
            response = Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        return response
