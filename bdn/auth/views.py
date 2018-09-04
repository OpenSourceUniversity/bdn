from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from .serializers import SignUpSerializer
from .models import SignUp


class SignUpViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    queryset = SignUp.objects.all()
    serializer_class = SignUpSerializer

    def create(self, request):
        data = request.data.copy()
        data['email'] = data['email'].lower()
        sign_up, _ = SignUp.objects.get_or_create(
                    email=data['email'])
        serializer = SignUpSerializer(
            data=data, instance=sign_up, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 'ok'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
