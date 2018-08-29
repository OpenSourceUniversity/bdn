from django.contrib import admin
from .models import Thread, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 1


class ThreadAdmin(admin.ModelAdmin):
    inlines = [MessageInline]


admin.site.register(Thread, ThreadAdmin)
