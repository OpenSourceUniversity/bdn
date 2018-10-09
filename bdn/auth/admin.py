from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, SignUp


class SignUpAdmin(admin.ModelAdmin):
    fields = [
        'email',
        'step',
        'email_sent',
        'modified',
    ]
    readonly_fields = ['modified']


admin.site.register(User, UserAdmin)
admin.site.register(SignUp, SignUpAdmin)
