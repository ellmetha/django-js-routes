from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path, re_path

from . import views


included_urlpatterns = [
    re_path(r'^test/(\d+)/foo/(\w+)/bar/$', views.ping, name='included_test_with_args'),
]

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^ping/$', views.ping, name='ping'),
    re_path(r'^ping/(\d+)/foo/(\w+)/bar/$', views.ping, name='ping_with_args'),
    re_path(r'^ping/(?P<pk1>\w+)/foo/(?P<pk2>\d+)/bar/$', views.ping, name='ping_with_kwargs'),
    re_path(r'^ping/(\d+)/fooo?/baa?r/$', views.ping, name='ping_with_optional_character'),
    re_path(r'^ping/(\d+)/foo(?:bar)?/$', views.ping, name='ping_with_optional_group'),
    re_path(r'^ping/(\d+)/(?:/(?P<op>[a-zA-Z]+)/)?$', views.ping, name='ping_with_optional_kwarg'),
    re_path(r'^included/(?P<pk1>\w+)/', include(included_urlpatterns)),
    path('ping/<int:year>/', views.ping, name='ping_with_path'),
    path('ping/<int:year>/<int:month>/', views.ping, name='ping_with_paths'),
    re_path(r'ping/(?P<year>[0-9]{4})/$', views.ping, name='ping_with_re_path'),
    path('ping/<slug>/', views.ping, name='ping_with_path_without_converter'),
]

urlpatterns += i18n_patterns(
    path('ping-i18n/', views.ping, name='ping_i18n'),
)
