from __future__ import unicode_literals

from collections import OrderedDict
from django.db.models import Q
from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import list_route, detail_route
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from bdn.auth.signature_authentication import SignatureAuthentication
from bdn.auth.models import User
from .models import Thread, Message
from .serializers import (
    ThreadSerializer, MessageGetSerializer,
    MessageSerializer, ThreadGetSerializer)


class ThreadViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = ThreadGetSerializer
    pagination_class = LimitOffsetPagination
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Thread.objects.filter(
            Q(owner=self.request.user) | Q(opponent=self.request.user))

    def destroy(self, request, pk=None):
        issuer = request.user
        thread_id = pk
        thread = get_object_or_404(Thread, id=thread_id)
        if thread.owner == issuer or thread.opponent == issuer:
            thread.delete()
            response = Response({'status': 'ok'})
        else:
            response = Response(
                {'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)
        return response

    def create(self, request):
        owner = request.user.id
        opponent_eth_address = str(
            request.data.get('opponent_eth_address')).lower()
        try:
            opponent = User.objects.get(
                username__iexact=opponent_eth_address).id
        except User.DoesNotExist:
            return Response({
                'error': 'User not found',
            }, status=status.HTTP_400_BAD_REQUEST)
        created_thread = Thread.objects.filter(
            Q(owner=owner, opponent=opponent) | Q(
                owner=opponent, opponent=owner)).first()
        if created_thread:
            serializer = ThreadGetSerializer(
                created_thread, context={'request': request})
            response = Response(serializer.data)
        else:
            serializer = ThreadSerializer(
                data={'owner': owner, 'opponent': opponent})
            if serializer.is_valid():
                serializer.save()
                response = Response(serializer.data)
            else:
                response = Response(serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)
        return response

    @list_route(methods=['get'])
    def get_unread_count(self, request):
        issuer = request.user
        unread_messages_count = Message.objects.all().filter(
            (Q(thread__owner=issuer) | Q(thread__opponent=issuer)) & Q(
                read=False)).exclude(sender=issuer).count()
        return Response({'unread_messages_count': unread_messages_count})


class MessagePagination(LimitOffsetPagination):
    default_limit = 30
    max_limit = 30

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class MessageViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = MessageGetSerializer
    pagination_class = MessagePagination
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        request = self.request
        thread_id = request.GET.get('thread_id')
        issuer = request.user
        thread = get_object_or_404(Thread, Q(
                pk=thread_id, owner=issuer) | Q(
                pk=thread_id, opponent=issuer))
        messages = Message.objects.filter(thread=thread)
        messages.exclude(sender=issuer).update(read=True)
        return messages

    @detail_route(methods=['post'])
    def mark_as_read_by_id(self, request, pk=None):
        issuer = request.user
        message = get_object_or_404(Message, pk=pk)
        if message.thread.owner == issuer or message.thread.opponent == issuer:
            message.read = True
            message.save()
        return Response({'message': message.pk})

    def create(self, request):
        thread_id = request.data.get('threadID')
        sender = request.user
        data = request.data.copy()
        thread = get_object_or_404(Thread, pk=thread_id)
        data['sender'] = sender.id
        data['thread'] = thread.id
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            message = serializer.save()
            thread.modified = timezone.now()
            thread.save()
            response = Response(MessageGetSerializer(message).data)
        else:
            response = Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        return response
