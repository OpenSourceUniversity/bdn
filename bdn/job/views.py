# Create your views here.
from uuid import UUID
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import list_route, detail_route
from bdn.auth.models import User
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from bdn.auth.utils import get_auth_eth_address
from haystack.query import SearchQuerySet
from bdn.auth.signature_authentication import SignatureAuthentication
from bdn.company.models import Company
from bdn.industry.models import Industry
from bdn.skill.models import Skill
from bdn.profiles.serializers import CompanyProfileSerializer
from .models import Job
from .serializers import JobSerializer, JobCreateSerializer


class JobViewSet(mixins.RetrieveModelMixin,
                 mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    pagination_class = LimitOffsetPagination
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)

    def retrieve(self, request, pk=None):
        job = get_object_or_404(Job, id=pk)
        user = job.company.user
        profile = user.profile
        serializerProfile = CompanyProfileSerializer(profile)
        serializerJob = JobSerializer(job)
        return Response({
            'job': serializerJob.data,
            'company': serializerProfile.data})

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        if search_query:
            sqs = SearchQuerySet().filter(title=search_query).models(Job)
            qs = [
                _.object
                for _ in sqs
            ]
            return qs

        qs = Job.objects.all()
        qs = qs.filter(self.industry_filter())
        qs = qs.filter(self.featured_filter())
        return qs

    def industry_filter(self):
        filtered_industries_ids = self.request.query_params.get(
            'filter_industry', '').split('|')
        industry_filter = Q()
        for filtered_industry_id in filtered_industries_ids:
            try:
                UUID(filtered_industry_id, version=4)
            except ValueError:
                continue
            industry_filter |= Q(industries__id=filtered_industry_id)
        return industry_filter

    def featured_filter(self):
        featured_filter = Q()
        if int(self.request.query_params.get('is_featured', 0)) == 1:
            featured_filter = Q(is_featured=True)
        return featured_filter

    @list_route(methods=['get'])
    def search(self, request):
        query = self.request.GET.get('q', '')
        sqs = SearchQuerySet().filter(title=query).models(Job)
        serializer = self.get_serializer([s.object for s in sqs], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def autocomplete(self, request):
        AUTOCOMPLETE_SIZE = 10
        sqs = SearchQuerySet().\
            filter(title_auto=request.GET.get('q', ''))\
            .models(Job)[:AUTOCOMPLETE_SIZE]
        serializer = self.get_serializer([
            s.object for s in sqs if s.object is not None], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def get_by_company(self, request):
        eth_address = str(request.GET.get('eth_address')).lower()
        business = get_object_or_404(User, username=eth_address)
        company = get_object_or_404(Company, user=business)
        sqs = Job.objects.all().filter(company=company)
        serializer = self.get_serializer([s for s in sqs], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @detail_route(methods=['get'])
    def get_by_id(self, request, pk=None):
        job_position = get_object_or_404(Job, id=pk)
        serializer = self.get_serializer(job_position)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @detail_route(methods=['post'])
    def edit_by_id(self, request, pk=None):
        eth_address = get_auth_eth_address(request.META)
        job_position = get_object_or_404(Job, id=pk)
        if job_position.company.user.username == eth_address:
            serializer = JobCreateSerializer(
                data=request.data, instance=job_position, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'ok'})
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)

    @detail_route(methods=['post'])
    def mark_featured_by_id(self, request, pk=None):
        eth_address = get_auth_eth_address(request.META)
        job_position = get_object_or_404(Job, id=pk)
        if job_position.company.user.username == eth_address:
            job_position.is_featured = True
            job_position.save()
        return Response({
            'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)

    @detail_route(methods=['post'])
    def delete_by_id(self, request, pk=None):
        eth_address = get_auth_eth_address(request.META)
        job_position = get_object_or_404(Job, id=pk)

        if job_position.company.user.username == eth_address:
            job_position.delete()
            return Response({'status': 'ok'})
        else:
            return Response({
                'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, pk=None):
        business = request.user
        try:
            company = Company.objects.get(user=business)
        except Company.DoesNotExist:
            return Response({
                'error': 'Company not found',
            }, status=status.HTTP_400_BAD_REQUEST)
        skills_post = request.data.get('skills', [])
        skills = Skill.objects.filter(name__in=skills_post)
        industries = Industry.objects.filter(
            name__in=request.data.get('industries', []))
        serializer = JobCreateSerializer(data=request.data)
        if serializer.is_valid():
            job = serializer.save(
                company=company, industries=industries, skills=skills)
            return Response({
                'status': 'ok',
                'pk': job.pk,
                })
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
