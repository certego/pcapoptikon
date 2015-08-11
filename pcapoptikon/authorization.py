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
