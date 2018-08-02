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
from bdn.certificate.views import CertificateViewSet
from bdn.profiles.views import ProfileViewSet
from bdn.course.views import CourseViewSet, CategoryViewSet
from bdn.job.views import JobViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'certificates', CertificateViewSet)
router.register(r'courses', CourseViewSet)
router.register(r'profile', ProfileViewSet)
router.register(r'categories', CategoryViewSet, base_name='Category')
router.register(r'jobs', JobViewSet)


urlpatterns = [
    path('api/v1/', include((router.urls, 'rest_framework'))),
    path('admin/', admin.site.urls),
]
