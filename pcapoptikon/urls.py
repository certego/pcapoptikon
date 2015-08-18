from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
admin.autodiscover()

from tastypie.api import Api
from main.api import *

v1_api = Api(api_name='v1')
v1_api.register(TaskResource())

urlpatterns = patterns('',
    # Admin views
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name="login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout_then_login', name="logout"),

    # APIs
    url(r'^api/', include(v1_api.urls)),

    # Other views
    url(r'', include('main.urls', namespace="main")),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
