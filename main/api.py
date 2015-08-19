#!/usr/bin/env python
#
# api.py
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
import os
from django.contrib.auth.models import User
from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.fields import ListField, ForeignKey
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication, SessionAuthentication, MultiAuthentication
from pcapoptikon.authorization import CertegoDjangoAuthorization
from pcapoptikon.fields import Base64FileField
from main.models import *

def is_post(bundle):
    if bundle.request.method == 'post':
        return True

class UserResource(ModelResource):
    class Meta:
        queryset        = User.objects.all()
        resource_name   = 'user'
        authentication  = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication(), SessionAuthentication())
        authorization   = CertegoDjangoAuthorization()
        allowed_methods = ['get']
        fields          = ['id', 'username']
        ordering        = ['id', 'username']

class TaskResource(ModelResource):
    pcap_file   = Base64FileField("pcap_file", use_in=is_post)
    user        = ForeignKey(UserResource, 'user', full=True)
    results     = ListField(attribute='results', null=True, blank=True, default=None)

    def obj_create(self, bundle, **kwargs):
        return super(TaskResource, self).obj_create(bundle, user=bundle.request.user)

    def alter_list_data_to_serialize(self, request, data):
        for item in data['objects']:
            item.data['filename'] = os.path.basename(Task.objects.get(pk=item.data['id']).pcap_file.name)
        return data

    class Meta:
        queryset = Task.objects.all().order_by('-id')
        resource_name = 'task'
        allowed_methods = ['get', 'post']
        authentication = MultiAuthentication(BasicAuthentication(), ApiKeyAuthentication(), SessionAuthentication())
        authorization = CertegoDjangoAuthorization()
        filtering = {
            'submitted_on': ALL,
            'user': ALL,
            'status': ALL,
        }
        ordering = ['id', 'submitted_on', 'status']
