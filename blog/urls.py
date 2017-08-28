from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from blog.views import PostViewSet, UserViewSet, CommentViewSet, TagViewSet
from . import views

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'users', UserViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'tags', TagViewSet)
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<post_id>[0-9a-fA-F-]+)/$', views.PostDetailView.as_view(), name='detail'),
    url(r'^edit/(?P<post_id>[0-9a-fA-F-]+)/$', views.edit, name='edit'),
    url(r'^api/', include(router.urls))
]
