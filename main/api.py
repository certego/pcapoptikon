from tastypie.resources import ModelResource, ALL, ALL_WITH_RELATIONS
from tastypie.fields import ListField
from tastypie.authentication import BasicAuthentication, ApiKeyAuthentication, SessionAuthentication, MultiAuthentication
from pcapoptikon.authorization import CertegoDjangoAuthorization
from pcapoptikon.fields import Base64FileField
from main.models import *

def is_post(bundle):
    if bundle.request.method == 'post':
        return True

class TaskResource(ModelResource):
    pcap_file   = Base64FileField("pcap_file", use_in=is_post)
    results     = ListField(attribute='results')

    def obj_create(self, bundle, **kwargs):
        return super(TaskResource, self).obj_create(bundle, user=bundle.request.user)

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
