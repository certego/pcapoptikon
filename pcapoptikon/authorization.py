#!/usr/bin/env python
#
# authorization.py
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
from django.contrib.auth.models import User
from tastypie.authorization import DjangoAuthorization
from tastypie.exceptions import Unauthorized

class CertegoDjangoAuthorization(DjangoAuthorization):
    def read_list(self, object_list, bundle):
        """
        Super-users can view the whole list; the others will only see their own tasks
        """
        user = bundle.request.user
        if not user.is_superuser:
            object_list = object_list.filter(user=bundle.request.user)

        return super(CertegoDjangoAuthorization, self).read_list(object_list, bundle)

    def read_detail(self, object_list, bundle):
        """
        Super-users can read any task; the others will only see their own
        """
        user = bundle.request.user

        if not user.is_superuser:
            object_list = object_list.filter(user=bundle.request.user)

        return super(CertegoDjangoAuthorization, self).read_detail(object_list, bundle)
