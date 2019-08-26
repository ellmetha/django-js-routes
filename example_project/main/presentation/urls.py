from django.urls import path, re_path

from . import views


urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('home/<int:year>/', views.HomeView.as_view(), name='home_with_arg'),
    path('home/<int:year>/<int:month>/', views.HomeView.as_view(), name='home_with_two_args'),
    re_path(r'home/(?P<year>[0-9]{4})/$', views.HomeView.as_view(), name='home_with_re_arg'),
    path('home/<slug>/', views.HomeView.as_view(), name='home_with_arg_without_converter'),
]
