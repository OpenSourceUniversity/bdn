from django.db.models import Q
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import list_route, detail_route
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from bdn.auth.utils import get_auth_eth_address
from bdn.auth.signature_authentication import SignatureAuthentication
from .models import Thread, Message
from .serializers import ThreadSerializer, MessageSerializer


class ThreadViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer
    pagination_class = LimitOffsetPagination
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Thread.objects.filter(
            Q(owner=self.request.user) | Q(opponent=self.request.user))
