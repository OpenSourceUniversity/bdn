# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from notifications.signals import notify
from bdn.auth.models import User
from bdn.auth.signature_authentication import SignatureAuthentication
from bdn.utils.send_email_tasks import rejected_certificate_email
from .models import Verification
from .serializers import VerificationSerializer, VerificationCreateSerializer


class VerificationViewSet(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = VerificationSerializer
    pagination_class = LimitOffsetPagination
    queryset = Verification.objects.none()

    @staticmethod
    def deny():
        return Response({
                    'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, pk=None):
        try:
            verification = Verification.objects.get(id=pk)
        except Verification.DoesNotExist:
            return Response({
                'error': 'Verification not found',
            }, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        if (verification.granted_to == user or verification.verifier == user):
            serializer = VerificationSerializer(verification)
            return Response(serializer.data)
        return self.deny()

    def list(self, request):
        user = request.user
        profile = str(request.GET.get('active_profile'))
        if profile == 'Academy':
            active_profile = 2
        elif profile == 'Business':
            active_profile = 3
        else:
            active_profile = 1
        verifications = Verification.objects.filter(
            verifier=user, certificate__isnull=False,
            verifier_type=active_profile).\
            order_by('state', 'date_last_modified')
        page = self.paginate_queryset(verifications)
        if page is not None:
            serializer = VerificationSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = VerificationSerializer(verifications, many=True)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def reject_by_id(self, request, pk=None):
        user = request.user
        verification = get_object_or_404(
            Verification, verifier=user, id=str(pk))
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
        if verification.granted_to.usersettings.subscribed:
            rejected_certificate_email.delay(
                verification.certificate.certificate_title,
                verification.verifier.profile.name_by_profile_type(
                    verification.verifier_type),
                verification.granted_to.email
                )
        return Response({'status': 'ok'})

    @detail_route(methods=['post'])
    def set_pending_by_id(self, request, pk=None):
        user = request.user
        verification = get_object_or_404(Verification, verifier=user, id=pk)
        verification.move_to_pending()
        verification.save()
        return Response({'status': 'ok'})

    @detail_route(methods=['post'])
    def set_open_by_id(self, request, pk=None):
        user = request.user
        verification = get_object_or_404(Verification, verifier=user, id=pk)
        verification.move_to_open()
        verification.save()
        return Response({'status': 'ok'})

    def create(self, request):
        data = request.data.copy()
        granted_to = request.user
        verifier = get_object_or_404(
            User, username__iexact=data['verifier'])
        if granted_to == verifier:
            return Response({
                'error': 'You are not able to verify certificate by yourself',
            }, status=status.HTTP_400_BAD_REQUEST)
        data['state'] = 'requested'
        data['granted_to'] = granted_to.id
        data['verifier'] = verifier.id
        verifier_type = int(data['verifier_type'])

        duplicate_verification = Verification.objects.filter(
            granted_to=granted_to,
            verifier=verifier, certificate__id=data['certificate'],
            granted_to_type=data['granted_to_type'],
            verifier_type=verifier_type).first()
        if duplicate_verification:
            return Response({
                'error': 'Duplicate verification request found',
                'id': duplicate_verification.id,
            }, status=status.HTTP_400_BAD_REQUEST)

        verifier_profile = verifier.profile

        if verifier_type == 1:
            return Response({
                'error': 'Wrong verifier profile type',
            }, status=status.HTTP_400_BAD_REQUEST)
        elif verifier_type == 2:
            if not (verifier_profile.academy_name and
                    verifier_profile.academy_website and
                    verifier_profile.academy_email):
                return Response({
                    'error': 'This Academy Profile is not created yet',
                }, status=status.HTTP_400_BAD_REQUEST)
        elif verifier_type == 3:
            if not (verifier_profile.company_name and
                    verifier_profile.company_website and
                    verifier_profile.company_email):
                return Response({
                    'error': 'This Business Profile is not created yet',
                }, status=status.HTTP_400_BAD_REQUEST)

        serializer = VerificationCreateSerializer(data=data)
        if serializer.is_valid():
            verification = serializer.save()
            granted_to_type = int(data['granted_to_type'])

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
