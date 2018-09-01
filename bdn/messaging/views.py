from django.db.models import Q
from django.utils import timezone
from rest_framework import status, viewsets, mixins
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
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Thread.objects.all()
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
        thread = Thread.objects.get(pk=thread_id)
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
            serializer = ThreadGetSerializer(instance=created_thread)
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


class MessageViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageGetSerializer
    pagination_class = LimitOffsetPagination
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        thread_id = request.GET.get('thread_id')
        try:
            thread = Thread.objects.get(
                Q(
                    pk=thread_id, owner=self.request.user) | Q(
                    pk=thread_id, opponent=self.request.user))
        except Thread.DoesNotExist:
            return Response({
                'error': 'Thread not found',
            }, status=status.HTTP_400_BAD_REQUEST)
        messages = Message.objects.filter(thread=thread)
        serializer = MessageGetSerializer(messages, many=True)
        return Response(serializer.data)

    def create(self, request):
        thread_id = request.data.get('threadID')
        sender = request.user
        data = request.data.copy()
        try:
            thread = Thread.objects.get(pk=thread_id)
        except Thread.DoesNotExist:
            return Response({
                'error': 'Thread not found',
            }, status=status.HTTP_400_BAD_REQUEST)
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
