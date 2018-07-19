from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from bdn.auth.signature_authentication import SignatureAuthentication
from rest_framework.response import Response
from .models import Certificate
from .serializers import CertificateSerializer


class CertificateViewSet(viewsets.ModelViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        eth_address = '0x' + str(request.META.get('HTTP_AUTH_ETH_ADDRESS')).lower()
        certificates = Certificate.objects.filter(user_eth_address=eth_address)
        serializer = CertificateSerializer(certificates, many=True)
        return Response(serializer.data)

    def create(self, request, pk=None):
        eth_address = '0x' + str(request.META.get('HTTP_AUTH_ETH_ADDRESS')).lower()
        serializer = CertificateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user_eth_address=eth_address)
            return Response({'status': 'ok'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)