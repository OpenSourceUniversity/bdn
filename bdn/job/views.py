from django.shortcuts import render

# Create your views here.
from uuid import UUID
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from haystack.query import SearchQuerySet
from bdn.auth.signature_authentication import SignatureAuthentication
from .models import Company, Job
from bdn.course.models import Skill, Category
from .serializers import CompanySerializer, JobSerializer
from bdn.course.serializers import SkillSerializer, CategorySerializer


class JobViewSet(viewsets.ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    pagination_class = LimitOffsetPagination
    # authentication_classes = (SignatureAuthentication,)
    # permission_classes = (IsAuthenticated,)

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
    def get_by_company(self, request):
        eth_address = request.GET.get('eth_address')
        company = Company.objects.get(eth_address = eth_address)
        sqs = Job.objects.all().filter(company=company)
        serializer = self.get_serializer([s for s in sqs], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @list_route(methods=['get'])
    def autocomplete(self, request):
        sqs = SearchQuerySet().filter(title_auto=request.GET.get('q', ''))[:10]
        serializer = self.get_serializer([s.object for s in sqs], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, pk=None):
        eth_address = '0x' + str(request.META.get('HTTP_AUTH_ETH_ADDRESS')).lower()
        company = Company.objects.get(eth_address = eth_address)
        skills_post = request.data.get('skills')
        skills_lower = []
        for skill in skills_post:
            skills_lower.append(skill.lower())
        print(skills_lower)
        skills = Skill.objects.filter(name__in=skills_lower)
        print(skills)
        categories = Category.objects.filter(name__in=request.data.get('categories'))
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(company=company, categories=categories, skills=skills)
            return Response({'status': 'ok'})
        else:
            print(serializer.errors)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
