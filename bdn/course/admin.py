from django.contrib import admin
from .models import Provider, Course, Category, Skill, Department

# Register your models here.
admin.site.register(Provider)
admin.site.register(Department)
admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Skill)
