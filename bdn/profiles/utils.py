from bdn.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from .models import Profile, ProfileType
from .serializers import (
    LearnerProfileSerializer, AcademyProfileSerializer,
    CompanyProfileSerializer)


def get_profile_by_type(pk, profile_type):
    SERIALIZERS = {
        ProfileType.ACADEMY: AcademyProfileSerializer,
        ProfileType.BUSINESS: CompanyProfileSerializer,
        ProfileType.LEARNER: LearnerProfileSerializer,
    }
    serializer_cls = SERIALIZERS[profile_type]
    eth_address = pk.lower()
    try:
        profile = Profile.objects.get(user__username__iexact=eth_address)
        serializer = serializer_cls(profile)
        response = Response(serializer.data)
    except User.DoesNotExist:
        response = Response(status=status.HTTP_400_BAD_REQUEST)
    return response
