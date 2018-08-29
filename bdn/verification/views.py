# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from notifications.signals import notify
from bdn.auth.models import User
from bdn.auth.signature_authentication import SignatureAuthentication
from bdn.auth.utils import get_auth_eth_address
from bdn.profiles.models import Profile
from .models import Verification
from .serializers import VerificationSerializer, VerificationCreateSerializer


class VerificationViewSet(viewsets.ModelViewSet):
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = VerificationSerializer
    queryset = Verification.objects.none()

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

    def retrieve(self, request, pk=None):
        eth_address = get_auth_eth_address(request.META)
        try:
            verification = Verification.objects.get(id=pk)
        except Verification.DoesNotExist:
            return Response({
                'error': 'Verification not found',
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=eth_address)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if (verification.granted_to == user or verification.verifier == user):
            serializer = VerificationSerializer(verification)
            return Response(serializer.data)
        return self.deny()

    def list(self, request):
        eth_address = get_auth_eth_address(request.META)
        try:
            user = User.objects.get(username=eth_address)
        except User.DoesNotExist:
            return Response({
                'error': 'User not found',
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            profile = Profile.objects.get(user=user)
        except User.DoesNotExist:
            return Response({
                'error': 'Profile not found',
            }, status=status.HTTP_400_BAD_REQUEST)
        verifications = Verification.objects.filter(
            verifier=user, certificate__isnull=False,
            verifier_type=profile.active_profile_type).\
            order_by('state', 'date_last_modified')
        serializer = VerificationSerializer(verifications, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def reject_by_id(self, request, pk=None):
        eth_address = get_auth_eth_address(request.META)
        try:
            user = User.objects.get(username=eth_address)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            verification = Verification.objects.get(
                verifier=user, id=str(pk))
        except Verification.DoesNotExist:
            return self.deny()
        verification.move_to_rejected()
        verification.save()
        notify.send(
            sender=verification.verifier,
            recipient=verification.granted_to,
            verb='rejected',
            target=verification.certificate,
            **{
                'actor_active_profile_type': verification.verifier_type,
                'recipient_active_profile_type': verification.granted_to_type,
            }
        )
        return Response({'status': 'ok'})

    @detail_route(methods=['post'])
    def set_pending_by_id(self, request, pk=None):
        eth_address = get_auth_eth_address(request.META)
        try:
            user = User.objects.get(username__iexact=eth_address)
        except User.DoesNotExist:
            return Response({
                'error': 'User not found',
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            verification = Verification.objects.get(
                verifier=user, id=pk)
        except Verification.DoesNotExist:
            return self.deny()
        verification.move_to_pending()
        verification.save()
        return Response({'status': 'ok'})

    def create(self, request):
        data = request.data.copy()
        eth_address = get_auth_eth_address(request.META)
        try:
            granted_to = User.objects.get(username__iexact=eth_address)
            verifier = User.objects.get(username__iexact=data['verifier'])
        except User.DoesNotExist:
            return Response({
                'error': 'User not found',
            }, status=status.HTTP_400_BAD_REQUEST)

        data['state'] = 'requested'
        data['granted_to'] = granted_to.id
        data['verifier'] = verifier.id

        duplicate_verification = Verification.objects.filter(
            granted_to=granted_to,
            verifier=verifier, certificate__id=data['certificate'],
            granted_to_type=data['granted_to_type'],
            verifier_type=data['verifier_type']).first()
        if duplicate_verification:
            return Response({
                'error': 'Duplicate verification request found',
                'id': duplicate_verification.id,
            }, status=status.HTTP_400_BAD_REQUEST)

        serializer = VerificationCreateSerializer(data=data)
        if serializer.is_valid():
            verification = serializer.save()
            granted_to_type = int(data['granted_to_type'])
            verifier_type = int(data['verifier_type'])

            notify.send(
                granted_to,
                recipient=verifier,
                verb='requested',
                action_object=verification,
                **{
                    'actor_active_profile_type': granted_to_type,
                    'recipient_active_profile_type': verifier_type,
                }
            )
            response = Response(serializer.data)
        else:
            response = Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return response
