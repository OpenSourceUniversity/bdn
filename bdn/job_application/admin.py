from django.contrib import admin
from .models import JobApplication


class JobApplicationAdmin(admin.ModelAdmin):
    list_display = [
        'job', 'issuer', 'state', 'date_created', 'date_last_modified',
    ]


admin.site.register(JobApplication, JobApplicationAdmin)
