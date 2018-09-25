# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from notifications.signals import notify
from bdn.auth.signature_authentication import SignatureAuthentication
from bdn.job.models import Job
from .models import JobApplication
from .serializers import (
    JobApplicationSerializer, JobApplicationViewSerializer,
    JobApplicationLearnerViewSerializer)


class JobApplicationPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 20

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class JobApplicationViewSet(mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = JobApplicationViewSerializer
    pagination_class = JobApplicationPagination

    @staticmethod
    def deny():
        return Response({
                    'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)

    def get_queryset(self):
        job_applications = JobApplication.objects.filter(
            job__company__user=self.request.user).\
            order_by('-date_created')
        return job_applications

    @list_route(methods=['get'])
    def get_by_user(self, request):
        user = request.user
        job_application = JobApplication.objects.filter(
                issuer=user).order_by('-date_created')
        serializer = JobApplicationLearnerViewSerializer(
            job_application, many=True)
        return Response({'results': serializer.data, })

    @detail_route(methods=['get'])
    def get_by_user_and_job(self, request, pk=None):
        user = request.user
        job_application = get_object_or_404(JobApplication,
                                            issuer=user, job=pk)
        serializer = JobApplicationSerializer(
            job_application)
        return Response(serializer.data)

    @detail_route(methods=['post'])
    def change_state_by_id(self, request, pk=None):
        user = request.user
        try:
            job_application = JobApplication.objects.get(
                job__company__user=user, id=pk)
        except JobApplication.DoesNotExist:
            return self.deny()
        state = request.GET.get('state')
        if state == 'reject':
            job_application.move_to_rejected()
            verb = 'rejected'
        else:
            job_application.move_to_approved()
            verb = 'approved'
        job_application.save()
        notify.send(
            job_application.job.company.user,
            recipient=job_application.issuer,
            verb=verb,
            action_object=job_application,
            **{
                'job_application_state': job_application.state,
                'actor_active_profile_type': 3,
                'recipient_active_profile_type': 1,
            }
        )
        return Response({'status': 'ok'})

    def create(self, request):
        issuer = request.user
        data = request.data.copy()
        data['issuer'] = issuer.id
        job = get_object_or_404(Job, id=data['job'])
        data['job'] = job.id
        duplicate_job_application = JobApplication.objects.filter(
            job=job, issuer=issuer).first()
        if duplicate_job_application:
            return Response({
                'error': 'Duplicate job application found',
                'id': duplicate_job_application.id,
            }, status=status.HTTP_400_BAD_REQUEST)
        serializer = JobApplicationSerializer(data=data)
        if serializer.is_valid():
            job_application = serializer.save()
            notify.send(
                issuer,
                recipient=job.company.user,
                verb='submitted',
                action_object=job_application,
                **{
                    'actor_active_profile_type': 1,
                    'recipient_active_profile_type': 3,
                }
            )
            response = Response(JobApplicationSerializer(job_application).data)
        else:
            print(serializer.errors)
            response = Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        return response
