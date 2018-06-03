from django.contrib import admin
from .models import Provider, Course, Category

# Register your models here.
admin.site.register(Provider)
admin.site.register(Course)
admin.site.register(Category)
