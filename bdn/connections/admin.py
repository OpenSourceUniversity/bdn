from django.contrib import admin
from .models import Connections, FileUpload

# Register your models here.
admin.site.register(Connections)
admin.site.register(FileUpload)
