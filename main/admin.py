#!/usr/bin/env python
#
# admin.py
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA  02111-1307  USA
#
# Author:   Pietro Delsante <p.delsante@certego.net>
#           www.certego.net
#
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
