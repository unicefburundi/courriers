"""courriers URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^courriers/', include('courriers_app.urls')),
    url(r'^', include('courriers_app.urls')),
    url(r'^login/$', auth_views.login,  name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^password_change/$', auth_views.PasswordChangeView.as_view(),  name='password_change'),
    url(r'^password_change_done/$', auth_views.PasswordChangeDoneView.as_view(),  name='password_change_done'),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(),  name='password_reset'),
    url(r'^password_reset_done/$', auth_views.PasswordResetDoneView.as_view(),  name='password_reset_done'),
    url(r'^password_reset_confirm/$', auth_views.PasswordResetConfirmView.as_view(),  name='password_reset_confirm'),
    url(r'^password_reset_complete/$', auth_views.PasswordResetCompleteView.as_view(),  name='password_reset_complete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)