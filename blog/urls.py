from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<post_id>[0-9a-fA-F-]+)/$', views.detail, name='detail'),
    url(r'^edit/(?P<post_id>[0-9a-fA-F-]+)/$', views.edit, name='edit'),
    url(r'^api/posts/$', views.api_post_list),
    url(r'^api/posts/(?P<pk>[0-9a-fA-F-]+)/$', views.api_post_detail)
]
