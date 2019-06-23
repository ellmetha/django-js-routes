from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path, re_path

from . import views


included_urlpatterns = [
    url(r'^test/(\d+)/foo/(\w+)/bar/$', views.ping, name='included_test_with_args'),
]

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^ping/$', views.ping, name='ping'),
    url(r'^ping/(\d+)/foo/(\w+)/bar/$', views.ping, name='ping_with_args'),
    url(r'^ping/(?P<pk1>\w+)/foo/(?P<pk2>\d+)/bar/$', views.ping, name='ping_with_kwargs'),
    url(r'^ping/(\d+)/fooo?/baa?r/$', views.ping, name='ping_with_optional_character'),
    url(r'^ping/(\d+)/foo(?:bar)?/$', views.ping, name='ping_with_optional_group'),
    url(r'^ping/(\d+)/(?:/(?P<op>[a-zA-Z]+)/)?$', views.ping, name='ping_with_optional_kwarg'),
    url(r'^included/(?P<pk1>\w+)/', include(included_urlpatterns)),
    path('ping/<int:year>/', views.ping, name='ping_with_path'),
    path('ping/<int:year>/<int:month>/', views.ping, name='ping_with_paths'),
    re_path(r'ping/(?P<year>[0-9]{4})/$', views.ping, name='ping_with_re_path'),
    path('ping/<slug>/', views.ping, name='ping_with_path_without_converter'),
]
