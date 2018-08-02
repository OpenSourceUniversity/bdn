from uuid import UUID
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from haystack.query import SearchQuerySet
from bdn.auth.signature_authentication import SignatureAuthentication
from .models import Course, Category, Provider, Skill
from .serializers import CourseSerializer, CategorySerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = LimitOffsetPagination
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        if search_query:
            qs = [
                _.object
                for _ in SearchQuerySet().filter(title=search_query)
            ]
            return qs
        else:
            qs = Course.objects.all()
        qs = qs.filter(self.category_filter())
        qs = qs.filter(self.featured_filter())
        return qs

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
    def get_by_provider(self, request):
        eth_address = request.GET.get('eth_address')
        provider = Provider.objects.get(eth_address=eth_address)
        sqs = Course.objects.all().filter(provider=provider)
        serializer = self.get_serializer([s for s in sqs], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @detail_route(methods=['get'])
    def get_by_id(self, request, pk=None):
        eth_address = '0x{0}'.format(
            str(request.META.get('HTTP_AUTH_ETH_ADDRESS')).lower())
        course_id = request.GET.get('id')
        course = Course.objects.get(id=course_id)
        if course.provider.eth_address == eth_address:
            serializer = self.get_serializer(course)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'denied'})

    @detail_route(methods=['post'])
    def edit_by_id(self, request, pk=None):
        eth_address = '0x{0}'.format(
            str(request.META.get('HTTP_AUTH_ETH_ADDRESS')).lower())
        course_id = request.data.get('id')
        course = Course.objects.get(id=course_id)
        if course.provider.eth_address == eth_address:
            serializer = self.get_serializer(
                data=request.data, instance=course, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'ok'})
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'denied'})

    def create(self, request, pk=None):
        eth_address = '0x{0}'.format(
            str(request.META.get('HTTP_AUTH_ETH_ADDRESS')).lower())
        provider = Provider.objects.get(eth_address=eth_address)
        skills_post = request.data.get('skills')
        skills_lower = []
        for skill in skills_post:
            skills_lower.append(skill.lower())
        skills = Skill.objects.filter(name__in=skills_lower)
        categories = Category.objects.filter(
            name__in=request.data.get('categories'))
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                provider=provider, categories=categories, skills=skills)
            return Response({'status': 'ok'})
        else:
            print(serializer.errors)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'])
    def delete_by_id(self, request, pk=None):
        eth_address = '0x{0}'.format(
            str(request.META.get('HTTP_AUTH_ETH_ADDRESS')).lower())
        course_id = request.data.get('id')
        course = Course.objects.get(id=course_id)
        if course.provider.eth_address == eth_address:
            course.delete()
            return Response({'status': 'ok'})
        else:
            return Response({'status': 'denied'})

    @list_route(methods=['get'])
    def autocomplete(self, request):
        sqs = SearchQuerySet().filter(title_auto=request.GET.get('q', ''))[:10]
        serializer = self.get_serializer([s.object for s in sqs], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
