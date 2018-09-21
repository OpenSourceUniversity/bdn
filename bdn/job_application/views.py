# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from notifications.signals import notify
from bdn.auth.signature_authentication import SignatureAuthentication
from bdn.job.models import Job
from .models import JobApplication
from .serializers import JobApplicationSerializer


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
    serializer_class = JobApplicationSerializer
    pagination_class = JobApplicationPagination

    def get_queryset(self):
        job_applications = JobApplication.objects.filter(
            job__company__user=self.request.user).\
            order_by('-date_created')
        return job_applications

    @detail_route(methods=['post'])
    def set_pending_by_id(self, request, pk=None):
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
            }
        )
        return Response({'status': 'ok'})

    def create(self, request):
        issuer = request.user
        data = request.data.copy()
        data['issuer'] = issuer
        job = get_object_or_404(Job, id=data['job'])
        data['job'] = job
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
                verb='applied',
                action_object=job_application,
            )
            response = Response(JobApplicationSerializer(job_application).data)
        else:
            response = Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        return response
