from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<post_id>[0-9a-fA-F-]+)/$', views.detail, name='detail'),
    url(r'^edit/(?P<post_id>[0-9a-fA-F-]+)/$', views.edit, name='edit'),
]

urlpatterns += format_suffix_patterns([
    url(r'^api/$', views.api_root),
    url(r'^api/posts/$', views.PostList.as_view(), name='post-list'),
    url(r'^api/posts/(?P<pk>[0-9a-fA-F-]+)/$', views.PostDetail.as_view(), name='post-detail'),
    url(r'^api/users/$', views.UserList.as_view(), name='user-list'),
    url(r'^api/users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
])
