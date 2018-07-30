from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.landing, name='landing'),
    url(r'^home$', views.home, name='home'),
    url(r'^new_mail$', views.new_mail, name='new_mail'),
    url(r'^track_mail$', views.track_mail, name='track_mail'),
    url(r'^save_mail$', views.save_mail, name='save_mail'),
]