from django.conf.urls import patterns, include, url
from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from main.api import *

v1_api = Api(api_name='v1')
v1_api.register(TaskResource())

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'pcapoptikon.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
