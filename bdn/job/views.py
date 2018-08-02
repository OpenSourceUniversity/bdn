# Create your views here.
from uuid import UUID
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from bdn.auth.utils import get_auth_eth_address
from haystack.query import SearchQuerySet
from bdn.auth.signature_authentication import SignatureAuthentication
from .models import Company, Job
from bdn.course.models import Skill, Category
from .serializers import JobSerializer
from bdn.course.serializers import CategorySerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    pagination_class = LimitOffsetPagination
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)

    def update(self, request):
        return Response({
                    'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)

    def partial_update(self, request):
        return Response({
                    'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request):
        return Response({
                    'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)

    def get_queryset(self):
        qs = Job.objects.all()
        qs = qs.filter(self.category_filter())
        return qs.filter(self.featured_filter())

    def category_filter(self):
        filtered_categories_ids = self.request.query_params.get(
            'filter_category', '').split('|')
        category_filter = Q()
        for filtered_category_id in filtered_categories_ids:
            try:
                UUID(filtered_category_id, version=4)
            except ValueError:
                continue
            if filtered_category_id:
                category_filter |= Q(categories__id=filtered_category_id)
        return category_filter

    def featured_filter(self):
        featured_filter = Q()
        if int(self.request.query_params.get('is_featured', 0)) == 1:
            featured_filter = Q(is_featured=True)
        return featured_filter

    @list_route(methods=['get'])
    def search(self, request):
        query = self.request.GET.get('q', '')
        sqs = SearchQuerySet().filter(title=query)
        serializer = self.get_serializer([s.object for s in sqs], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def autocomplete(self, request):
        sqs = SearchQuerySet().filter(title_auto=request.GET.get('q', ''))[:10]
        serializer = self.get_serializer([s.object for s in sqs], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def get_by_company(self, request):
        eth_address = str(request.GET.get('eth_address')).lower()
        company = Company.objects.get(eth_address=eth_address)
        sqs = Job.objects.all().filter(company=company)
        serializer = self.get_serializer([s for s in sqs], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @detail_route(methods=['get'])
    def get_by_id(self, request, pk=None):
        eth_address = get_auth_eth_address(request.META)
        job_id = pk
        job_position = Job.objects.get(id=job_id)
        if job_position.company.eth_address == eth_address:
            serializer = self.get_serializer(job_position)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)

    @detail_route(methods=['post'])
    def edit_by_id(self, request, pk=None):
        eth_address = get_auth_eth_address(request.META)
        job_id = pk
        job_position = Job.objects.get(id=job_id)
        if job_position.company.eth_address == eth_address:
            serializer = self.get_serializer(
                data=request.data, instance=job_position, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'ok'})
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)

    @detail_route(methods=['post'])
    def delete_by_id(self, request, pk=None):
        eth_address = get_auth_eth_address(request.META)
        job_id = pk
        job_position = Job.objects.get(id=job_id)
        if job_position.company.eth_address == eth_address:
            job_position.delete()
            return Response({'status': 'ok'})
        else:
            return Response({
                'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, pk=None):
        eth_address = get_auth_eth_address(request.META)
        company = Company.objects.get(eth_address=eth_address)
        skills_post = request.data.get('skills')
        skills_lower = []
        for skill in skills_post:
            skills_lower.append(skill.lower())
        skills = Skill.objects.filter(name__in=skills_lower)
        categories = Category.objects.filter(
            name__in=request.data.get('categories'))
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                company=company, categories=categories, skills=skills)
            return Response({'status': 'ok'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
