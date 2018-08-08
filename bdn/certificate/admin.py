from django.contrib import admin
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin
from .models import Certificate


@admin.register(Certificate)
class CertificateAdmin(AjaxSelectAdmin):

    form = make_ajax_form(Certificate, {
        'skills': 'skills'
    })
