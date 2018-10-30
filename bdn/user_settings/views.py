from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.decorators import list_route
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import (IsAuthenticated,
                                        AllowAny)
from bdn.auth.signature_authentication import SignatureAuthentication
from bdn.auth.models import User
from .serializers import UserSettingsSerializer, UserSettingsWalletSerializer
from .models import UserSettings


class UserSettingsViewSet(mixins.CreateModelMixin,
                          viewsets.GenericViewSet,
                          mixins.ListModelMixin):
    queryset = UserSettings.objects.all()
    serializer_class = UserSettingsSerializer
    authentication_classes = (SignatureAuthentication,)

    def get_permissions(self):
        if self.action and (self.action in ('get_wallet',)):
            self.permission_classes = [AllowAny, ]
        else:
            self.permission_classes = [IsAuthenticated, ]
        return super(self.__class__, self).get_permissions()

    @list_route(methods=['post'])
    def get_wallet(self, request):
        user_email = request.data['email']
        if not user_email:
            return Response({'error': 'Wallet not stored'},
                            status=status.HTTP_400_BAD_REQUEST)
        user = get_object_or_404(User, email=user_email)
        user_settings = get_object_or_404(UserSettings, user=user)
        if user_settings.password:
            if check_password(
                    request.data['password'], user_settings.password):
                wallet_serializer = UserSettingsWalletSerializer(user_settings)
                return Response(wallet_serializer.data)
            return Response({'error': 'Wrong password'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Wallet not stored'},
                        status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['post'])
    def set_wallet(self, request):
        user_settings = get_object_or_404(UserSettings, user=request.user)
        try:
            request.data['isRecovery']
            if user_settings.save_wallet:
                password = make_password(request.data['password'])
                wallet = request.data['wallet']
                user_settings.password = password
                user_settings.wallet = wallet
                user_settings.save()
                return Response({'status': 'ok'})
            else:
                user_settings.password = None
                user_settings.wallet = None
                user_settings.save()
                return Response({'status': 'ok'})
        except KeyError:
            if request.data['save_wallet']:
                password = make_password(request.data['password'])
                wallet = request.data['wallet']
                user_settings.password = password
                user_settings.wallet = wallet
                user_settings.save()
                return Response({'status': 'ok'})
            else:
                user_settings.password = None
                user_settings.wallet = None
                user_settings.save()
                return Response({'status': 'ok'})

    def list(self, request):
        user_settings = get_object_or_404(UserSettings, user=request.user)
        serializer_user_settings = UserSettingsSerializer(user_settings)
        return Response(serializer_user_settings.data)

    def create(self, request):
        user_settings = UserSettings.objects.get(
                    user=request.user)
        if (request.user.email != request.data['email']):
            user = User.objects.filter(email=request.data['email']).first()
            if user:
                return Response(
                    {'error': 'Email duplicate, please use another one'},
                    status=status.HTTP_400_BAD_REQUEST)
            else:
                request.user.email = request.data['email']
                request.user.save()
        serializer = UserSettingsSerializer(
            data=request.data, instance=user_settings, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'ok'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
