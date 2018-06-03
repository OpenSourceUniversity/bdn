from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from .models import Course
from .serializers import CourseSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = LimitOffsetPagination
