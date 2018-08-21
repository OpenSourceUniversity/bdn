# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from bdn.auth.signature_authentication import SignatureAuthentication
from bdn.auth.utils import get_auth_eth_address
from notifications.models import Notification
from .serializers import NotificationSerializer


class NotificationPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 20


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = NotificationPagination

    def retrieve(self, request, pk=None):
        eth_address = get_auth_eth_address(request.META)
        notification = Notification.objects.get(
            id=pk, recipient__username__iexact=eth_address.lower())
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)

    def get_queryset(self):
        request = self.request
        eth_address = get_auth_eth_address(request.META)
        notifications = Notification.objects\
            .filter(recipient__username__iexact=eth_address.lower())\
            .order_by('-timestamp')
        return notifications

    def update(self, request):
        return self.deny()

    def partial_update(self, request):
        return self.deny()

    def destroy(self, request):
        return self.deny()

    @staticmethod
    def deny():
        return Response({
            'status': 'denied'
        }, status=status.HTTP_401_UNAUTHORIZED)
