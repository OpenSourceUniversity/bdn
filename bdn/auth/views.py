from rest_framework import status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from bdn.auth.signature_authentication import SignatureAuthentication
from bdn.auth.models import User
from bdn.utils.send_email_tasks import verification_email_on_create
from .serializers import SignUpSerializer
from .models import SignUp


class SignUpViewSet(mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    queryset = SignUp.objects.all()
    serializer_class = SignUpSerializer
    authentication_classes = (SignatureAuthentication,)
    permission_classes = (AllowAny,)

    def create(self, request):
        data = request.data.copy()
        data['email'] = data['email'].lower()
        user = User.objects.filter(email__iexact=data['email']).first()
        if user:
            return Response(
                {'error': 'Email duplicate, please use another one'},
                status=status.HTTP_400_BAD_REQUEST)
        else:
            sign_up, _ = SignUp.objects.get_or_create(
                        email__iexact=data['email'])
            if not (request.user.is_anonymous) and not (request.user.email):
                request.user.email = data['email']
                request.user.save()
                request.user.profile.learner_email = data['email']
                request.user.profile.save()
                if not (request.user.usersettings.email_verified):
                    verification_email_on_create.delay(
                        request.user.usersettings.email_verification_link,
                        request.user.email
                        )
            serializer = SignUpSerializer(
                data=data, instance=sign_up, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'status': 'ok'})
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)
