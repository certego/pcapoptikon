from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.authentication import ApiKeyAuthentication
from pcapoptikon.authorization import CertegoDjangoAuthorization
from pcapoptikon.fields import Base64FileField
from main.models import *

class TaskResource(ModelResource):
    pcap_file = Base64FileField("pcap_file")

    def obj_create(self, bundle, **kwargs):
        return super(TaskResource, self).obj_create(bundle, user=bundle.request.user)

    class Meta:
        queryset = Task.objects.all().order_by('-id')
        resource_name = 'task'
        allowed_methods = ['get', 'post']
        authentication = ApiKeyAuthentication()
        authorization = CertegoDjangoAuthorization()
        filtering = {
            'submitted_on': ALL,
            'user': ALL,
            'status': ALL,
        }
