from tastypie.admin import ApiKeyInline
from tastypie.models import ApiAccess, ApiKey
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib import admin
from .models import Task


class TaskAdmin(admin.ModelAdmin):
    list_display = ['id', 'pcap_file', 'submitted_on', 'user', 'status', 'results_dir']
    list_editable = ['user', 'status']
    list_filter = ['user', 'status']
    search_fields = ['pcap_file', 'results']
    date_hierarchy = 'submitted_on'

class UserModelAdmin(UserAdmin):
    inlines = UserAdmin.inlines + [ApiKeyInline]

#admin.site.register(ApiKey)
admin.site.register(ApiAccess)
admin.site.unregister(User)
admin.site.register(User,UserModelAdmin)
admin.site.register(Task, TaskAdmin)
