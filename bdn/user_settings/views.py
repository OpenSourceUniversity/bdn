from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from rest_framework.decorators import list_route
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from bdn.auth.signature_authentication import SignatureAuthentication
from .serializers import UserSettingsSerializer, UserSettingsWalletSerializer
from .models import UserSettings


class UserSettingsViewSet(mixins.CreateModelMixin,
                          viewsets.GenericViewSet,
                          mixins.RetrieveModelMixin):
    queryset = UserSettings.objects.all()
    serializer_class = UserSettingsSerializer
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)

    @list_route(methods=['get'])
    def get_wallet(self, request):
        user_settings = get_object_or_404(UserSettings, user=request.user)
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
        if user_settings.save_wallet:
            password = make_password(request.data['password'])
            wallet = request.data['wallet']
            user_settings.password = password
            user_settings.wallet = wallet
            user_settings.save()
            return Response({'status': 'ok'})
        else:
            return Response({'error': 'Wallet is private'},
                            status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        user_settings = get_object_or_404(UserSettings, user=request.user)
        serializer_user_settings = UserSettingsSerializer(user_settings)
        return Response(serializer_user_settings.data)

    def create(self, request):
        user_settings = UserSettings.objects.get(
                    user=request.user)
        if request.data['save_wallet']:
            if request.data['password']:
                password = make_password(request.data['password'])
                user_settings.password = password
                user_settings.save()
        else:
            user_settings.password = None
            user_settings.wallet = None
            user_settings.save()
        serializer = UserSettingsSerializer(
            data=request.data, instance=user_settings, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'ok'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
