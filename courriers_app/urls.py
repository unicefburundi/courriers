from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.landing, name='landing'),
    url(r'^home$', views.home, name='home'),
    url(r'^new_mail$', views.new_mail, name='new_mail'),
    url(r'^new_mail_1$', views.new_mail_1, name='new_mail_1'),
    url(r'^partners$', views.partners, name='partners'),
    url(r'^transfer_mail$', views.transfer_mail, name='transfer_mail'),
    url(r'^transfer_mail_1$', views.transfer_mail_1, name='transfer_mail_1'),
    url(r'^save_mail$', views.save_mail, name='save_mail'),
    url(r'^save_mail_1$', views.save_mail_1, name='save_mail_1'),
    url(r'^get_unclosed_mails$', views.get_unclosed_mails, name='get_unclosed_mails'),
    url(r'^get_closed_mails$', views.get_closed_mails, name='get_closed_mails'),
    url(r'^save_transfer$', views.save_transfer, name='save_transfer'),
    url(r'^save_transfer_1$', views.save_transfer_1, name='save_transfer_1'),
    url(r'^search_mail$', views.search_mail, name='search_mail'),
    url(r'^track_mails$', views.track_mails, name='track_mails'),
    url(r'^close_mail_view$', views.close_mail_view, name='close_mail_view'),
    url(r'^close_mail$', views.close_mail, name='close_mail'),
    url(r'^stat_all_mails$', views.stat_all_mails, name='stat_all_mails'),
    url(r'^stat_closed_mails$', views.stat_closed_mails, name='stat_closed_mails'),
    url(r'^stat_not_closed_mails$', views.stat_not_closed_mails, name='stat_not_closed_mails'),
    url(r'^mail_details/(?P<mail_number>)$', views.mail_details, name='mail_details'),
    url(r'^mail_details/(?P<mail_number>)$', views.mail_details, name='mail_details'),
    url(
        r'^get_on_process_mails_for_staff/(?P<staff_id>)$', 
        views.get_on_process_mails_for_staff, 
        name='get_on_process_mails_for_staff'
        ),
    url(r'^all_mails$', views.MailListView.as_view(), name='all_mails'),
    url(r'^all_mails_types$', views.MailTypeListView.as_view(), name='all_mails_types'),
]