from uuid import UUID
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import list_route
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from haystack.query import SearchQuerySet
from .models import Course, Category
from .serializers import CourseSerializer, CategorySerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        qs = Course.objects.all()
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


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
