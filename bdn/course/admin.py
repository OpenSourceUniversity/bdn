from django.contrib import admin
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin
from .models import Course


@admin.register(Course)
class CourseAdmin(AjaxSelectAdmin):

    form = make_ajax_form(Course, {
        'skills': 'skills'
    })
