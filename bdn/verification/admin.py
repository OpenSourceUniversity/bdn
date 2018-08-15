from django.contrib import admin
from .models import Verification


class VerificationAdmin(admin.ModelAdmin):
    list_display = [
        'date_created', 'state', 'tx_hash', 'granted_to', 'verifier',
    ]


admin.site.register(Verification, VerificationAdmin)
