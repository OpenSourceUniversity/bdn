from django.contrib import admin
from .models import Connection, FileUpload

# Register your models here.
admin.site.register(Connection)
admin.site.register(FileUpload)
