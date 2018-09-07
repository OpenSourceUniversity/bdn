"""bdn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from ajax_select import urls as ajax_select_urls
from bdn.certificate.views import CertificateViewSet
from bdn.profiles.views import ProfileViewSet
from bdn.industry.views import IndustryViewSet
from bdn.course.views import CourseViewSet
from bdn.skill.views import SkillViewSet
from bdn.job.views import JobViewSet
from bdn.connections.views import ConnectionsViewSet, FileViewSet
from bdn.verification.views import VerificationViewSet
from bdn.auth.views import SignUpViewSet
from bdn.messaging.views import ThreadViewSet, MessageViewSet
from bdn.notifications_extensions.views import NotificationViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'certificates', CertificateViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'profile', ProfileViewSet)
router.register(r'industries', IndustryViewSet, base_name='Industry')
router.register(r'skills', SkillViewSet, base_name='Skill')
router.register(r'jobs', JobViewSet)
router.register(r'connections', ConnectionsViewSet)
router.register(r'archive', FileViewSet, base_name='archive')
router.register(r'verifications', VerificationViewSet)
router.register(r'messaging/threads', ThreadViewSet, base_name='Thread')
router.register(
    r'notifications', NotificationViewSet, base_name='Notification')
router.register(r'signup', SignUpViewSet)
router.register(r'messages', MessageViewSet, base_name='Message')


urlpatterns = [
    path('api/v1/', include((router.urls, 'rest_framework'))),
    path('ajax_select/', include(ajax_select_urls)),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
