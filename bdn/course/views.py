from uuid import UUID
from django.db.models import Q
from rest_framework import status, viewsets
from rest_framework.decorators import list_route, detail_route
from bdn.auth.models import User
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from haystack.query import SearchQuerySet
from bdn.auth.signature_authentication import SignatureAuthentication
from bdn.auth.utils import get_auth_eth_address
from bdn.profiles.models import Profile
from bdn.industry.models import Industry
from bdn.skill.models import Skill
from bdn.provider.models import Provider
from bdn.profiles.serializers import AcademyProfileSerializer
from .serializers import CourseSerializer
from .models import Course


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
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

    def retrieve(self, request, pk=None):
        try:
            course = Course.objects.get(id=pk)
        except Course.DoesNotExist:
            return Response({
                'error': 'Course not found',
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(username=course.provider.eth_address)
        except User.DoesNotExist:
            return Response({
                'error': 'User not found',
            }, status=status.HTTP_400_BAD_REQUEST)
        profile = Profile.objects.get(user=user)
        serializerProfile = AcademyProfileSerializer(profile)
        serializerCourse = CourseSerializer(course)
        return Response({
            'course': serializerCourse.data,
            'academy': serializerProfile.data
        })

    def get_queryset(self):
        search_query = self.request.GET.get('q', '')
        if search_query:
            sqs = SearchQuerySet().filter(title=search_query).models(Course)
            qs = [
                _.object
                for _ in sqs
            ]
            return qs

        qs = Course.objects.all()
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
            if filtered_industry_id:
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
        sqs = SearchQuerySet().filter(title=query).models(Course)
        serializer = self.get_serializer([s.object for s in sqs], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def autocomplete(self, request):
        AUTOCOMPLETE_SIZE = 10
        sqs = SearchQuerySet()\
            .filter(title_auto=request.GET.get('q', ''))\
            .models(Course)[:AUTOCOMPLETE_SIZE]
        serializer = self.get_serializer([s.object for s in sqs], many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @list_route(methods=['get'])
    def get_by_provider(self, request):
        eth_address = str(request.GET.get('eth_address')).lower()
        try:
            academy = User.objects.get(username=eth_address)
        except User.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        try:
            provider = Provider.objects.get(user=academy)
        except Provider.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        qs = Course.objects.all().filter(provider=provider)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @detail_route(methods=['get'])
    def get_by_id(self, request, pk=None):
        eth_address = get_auth_eth_address(request.META)
        course_id = pk
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({
                'error': 'Course not found',
            }, status=status.HTTP_400_BAD_REQUEST)
        if course.provider.eth_address == eth_address:
            serializer = self.get_serializer(course)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)

    @detail_route(methods=['post'])
    def edit_by_id(self, request, pk=None):
        eth_address = get_auth_eth_address(request.META)
        course_id = pk
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({
                'error': 'Course not found',
            }, status=status.HTTP_400_BAD_REQUEST)
        if course.provider.eth_address == eth_address:
            serializer = self.get_serializer(
                data=request.data, instance=course, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'ok'})
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({
            'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, pk=None):
        eth_address = get_auth_eth_address(request.META)
        try:
            provider = Provider.objects.get(eth_address=eth_address)
        except Provider.DoesNotExist:
            return Response({
                'error': 'Provider not found',
            }, status=status.HTTP_400_BAD_REQUEST)
        skills_post = request.data.get('skills')
        skills_lower = [_.lower() for _ in skills_post]
        skills = Skill.objects.filter(name__in=skills_lower)
        industries = Industry.objects.filter(
            name__in=request.data.get('industries'))
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(
                provider=provider, industries=industries, skills=skills)
            return Response({'status': 'ok'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'])
    def delete_by_id(self, request, pk=None):
        eth_address = get_auth_eth_address(request.META)
        course_id = pk
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response({
                'error': 'Course not found',
            }, status=status.HTTP_400_BAD_REQUEST)
        if course.provider.eth_address == eth_address:
            course.delete()
            return Response({'status': 'ok'})
        else:
            return Response(
                {'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)
