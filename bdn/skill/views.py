from haystack.query import SearchQuerySet
from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import list_route
from .models import Skill
from .serializers import SkillSerializer


class SkillViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

    @list_route(methods=['get'])
    def autocomplete(self, request):
        AUTOCOMPLETE_SIZE = 10
        query = request.GET.get('q', '')
        if not query:
            sqs = Skill.objects.none()
        else:
            sqs = SearchQuerySet()\
                .filter(name_auto=query, standardized=True)\
                .models(Skill)[:AUTOCOMPLETE_SIZE]
        serializer = self.get_serializer(sqs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
