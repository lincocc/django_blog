from django.conf.urls import url, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(template_name="blog/auth/login.html"), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name="blog/auth/logout.html"), name='logout'),
    # url('^', include('django.contrib.auth.urls')),
]
