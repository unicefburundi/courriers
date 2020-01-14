# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from courriers_app.models import *
from import_export.admin import ImportExportModelAdmin


@admin.register(Sender)
class SenderAdmin(ImportExportModelAdmin):
	pass

admin.site.register(StaffPosition)
admin.site.register(Section)
admin.site.register(Staff)
admin.site.register(Mail)
admin.site.register(Track)
admin.site.register(MailType)