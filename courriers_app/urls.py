from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.landing, name='landing'),
    url(r'^home$', views.home, name='home'),
    url(r'^new_mail$', views.new_mail, name='new_mail'),
    url(r'^transfer_mail$', views.transfer_mail, name='transfer_mail'),
    url(r'^save_mail$', views.save_mail, name='save_mail'),
    url(r'^get_mails$', views.get_mails, name='get_mails'),
    url(r'^save_transfer$', views.save_transfer, name='save_transfer'),
]