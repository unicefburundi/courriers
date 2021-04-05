import django_tables2 as tables
from courriers_app.models import *


class MailTable(tables.Table):
    class Meta:
        model = Mail
        template_name = "all_mails.html"
        #fields = ("external_number", "number",)


class MailTypeTable(tables.Table):
    class Meta:
        model = MailType
        template_name = "all_mail_types.html"