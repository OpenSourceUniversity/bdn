from rest_framework import viewsets
from bdn.industry.models import Industry
from bdn.industry.serializers import IndustrySerializer


class IndustryViewSet(viewsets.ModelViewSet):
    queryset = Industry.objects.all().order_by('name')
    serializer_class = IndustrySerializer
