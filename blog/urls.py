from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from blog.views import PostViewSet, UserViewSet
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<post_id>[0-9a-fA-F-]+)/$', views.detail, name='detail'),
    url(r'^edit/(?P<post_id>[0-9a-fA-F-]+)/$', views.edit, name='edit'),
]

post_list = PostViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

post_detail = PostViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

user_list = UserViewSet.as_view({
    'get': 'list'
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})
urlpatterns += format_suffix_patterns([
    url(r'^api/$', views.api_root),
    url(r'^api/posts/$', post_list, name='post-list'),
    url(r'^api/posts/(?P<pk>[0-9a-fA-F-]+)/$', post_detail, name='post-detail'),
    url(r'^api/users/$', user_list, name='user-list'),
    url(r'^api/users/(?P<pk>[0-9]+)/$', user_detail, name='user-detail'),
])
