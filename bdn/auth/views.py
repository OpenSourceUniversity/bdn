from rest_framework import status, viewsets
from rest_framework.response import Response
from .serializers import SignUpSerializer
from .models import SignUp


class SignUpViewSet(viewsets.ModelViewSet):
    queryset = SignUp.objects.all()
    serializer_class = SignUpSerializer

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
        return Response({
                    'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)

    def list(self, request, pk=None):
        return Response({
                    'status': 'denied'}, status=status.HTTP_401_UNAUTHORIZED)

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
