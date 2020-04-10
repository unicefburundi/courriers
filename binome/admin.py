# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from binome.models import *
from import_export.admin import ImportExportModelAdmin


@admin.register(Binome)
class BinomeAdmin(ImportExportModelAdmin):
	pass

@admin.register(NotAvailable)
class NotAvailableAdmin(ImportExportModelAdmin):
	pass
