from django.contrib import admin
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin
from .models import Job


@admin.register(Job)
class JobAdmin(AjaxSelectAdmin):

    form = make_ajax_form(Job, {
        'skills': 'skills'
    })
