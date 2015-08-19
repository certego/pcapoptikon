#!/usr/bin/env python
#
# urls.py
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
from django.conf.urls import patterns, url

from main import views

urlpatterns = patterns('',
    url(r'^task/((?P<task_id>\d+)/)?$', views.task, name='task'),
    url(r'^new_task/$', views.new_task, name='new_task'),
    url(r'^$', views.tasks, name='tasks'),
)
