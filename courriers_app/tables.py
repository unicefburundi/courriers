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


class SectionTable(tables.Table):
    class Meta:
        model = Section
        template_name = "all_sections.html"


class SenderTable(tables.Table):
    class Meta:
        model = Sender
        template_name = "all_senders.html"

class StaffPositionTable(tables.Table):
    class Meta:
        model = StaffPosition
        template_name = "all_staff_positions.html"


class StaffTable(tables.Table):
    class Meta:
        model = Staff
        template_name = "all_staffs.html"


class TrackTable(tables.Table):
	class Meta:
		#model = Track
		sequence = ("mail__id", "staff__id", )
		template_name = "all_tracks.html"