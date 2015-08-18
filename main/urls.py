from django.conf.urls import patterns, url

from main import views

urlpatterns = patterns('',
    url(r'^task/(?P<asset_id>\d+)/$', views.task, name='task'),
    url(r'^new_task/$', views.new_task, name='new_task'),
    url(r'^$', views.tasks, name='tasks'),
)
