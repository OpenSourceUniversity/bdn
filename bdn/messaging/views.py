from django.db.models import Q
from django.utils import timezone
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import list_route, detail_route
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from bdn.auth.utils import get_auth_eth_address
from bdn.auth.signature_authentication import SignatureAuthentication
from bdn.auth.models import User
from .models import Thread, Message
from .serializers import ThreadSerializer, MessageSerializer


class ThreadViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
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

    def create(self, request, pk=None):
        owner = request.user
        opponent_eth_address = str(pk).lower()
        try:
            opponent = User.objects.get(username__iexact=opponent_eth_address)
        except User.DoesNotExist:
            return Response({
                'error': 'User not found',
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer = ThreadSerializer(
            data={'owner': owner, 'opponent': opponent})
        if serializer.is_valid():
            serializer.save()
            response = Response({'status': 'ok'})
        else:
            response = Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        return response


class MessageViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    pagination_class = LimitOffsetPagination
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request, thread_pk=None):
        sender = request.user
        data = request.data.copy()
        try:
            thread = Thread.objects.get(pk=thread_pk)
        except Thread.DoesNotExist:
            return Response({
                'error': 'Thread not found',
            }, status=status.HTTP_400_BAD_REQUEST)
        data['sender'] = sender
        data['thread'] = thread
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            thread.modified = timezone.now()
            thread.save()
            response = Response({'status': 'ok'})
        else:
            response = Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        return response
