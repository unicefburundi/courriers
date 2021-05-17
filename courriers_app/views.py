# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from courriers_app.models import *
from forms import *
from django.http import HttpResponse
import json
from django.db.models import F, Count, Func, Sum, Q
import datetime
from django.core import serializers
import unicodedata
from django.core.mail import send_mail

from django.core.files.storage import FileSystemStorage
from django.db.models import Max
from django.views.generic import ListView
from courriers_app.tables import *
from django_tables2 import SingleTableView



class DiffDays(Func):
    function = 'DATE_PART'
    template = "%(function)s('day', %(expressions)s)"

class CastDate(Func):
    function = 'date_trunc'
    template = "%(function)s('day', %(expressions)s)"

# Create your views here.
def landing(request):
    d = {}
    return render(request, 'landing_page.html', d)

def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError

def home(request):
    d = {}
    return render(request, 'home.html', d)

def new_mail(request):
    if request.method == 'POST':
        mail_type = request.POST.get('mail_type')
        sender = request.POST.get('sender')

    d = {}
    d["pagetitle"] = "New mails"
    d["mail_types"] = MailType.objects.all()
    d["senders"] = Sender.objects.all()
    d["mails"] = Mail.objects.all()
    d["mails"] = (Mail.objects.all()
        .annotate(sender_f_name = F('sender__first_name'))
        .annotate(sender_l_name = F('sender__last_name'))
        .annotate(mail_type_name = F('mail_type__mail_type_name'))
        )
    d["mails"] = d["mails"].values()
    d["mails"] = json.dumps(list(d["mails"]), default=date_handler)
    return render(request, 'new_mail.html', d)


def new_mail_1(request):
    d = {}
    message_to_user = ""
    if request.method == 'POST':
        mail_type = request.POST.get('mail_type')
        sender = request.POST.get('sender')
        external_number = request.POST.get('external_mail_number')
        internal_number = request.POST.get('mail_number')
        reception_date_time = request.POST.get('date_time_picked')
        answer_needed = request.POST.get('answer_needed')
        soft_copy = request.FILES['soft_copy'] if 'soft_copy' in request.FILES else False

        if not reception_date_time:
            message_to_user = "Error. You have not selected the reception date and time"
            d["pagetitle"] = "New mails"
            d["mail_types"] = MailType.objects.all()
            d["senders"] = Sender.objects.all().order_by("first_name")
            d["mails"] = (Mail.objects.filter(track = None)
                .annotate(sender_f_name = F('sender__first_name'))
                .annotate(sender_l_name = F('sender__last_name'))
                .annotate(mail_type_name = F('mail_type__mail_type_name'))
                )
            d["mails"] = d["mails"].values()
            d["mails"] = json.dumps(list(d["mails"]), default=date_handler)
            d["message_to_user"] = message_to_user
            return render(request, 'new_mail_1.html', d)

        reception_date_time = unicodedata.normalize('NFKD', reception_date_time).encode('ascii','ignore')
        reception_date_time = datetime.datetime.strptime(reception_date_time, '%m/%d/%Y %I:%M %p')

        if answer_needed is None:
            the_answer_is_needed = False
        else:
            the_answer_is_needed = True

        #Let's identify the connected staff
        the_connected_user = request.user
        the_connected_staff = Staff.objects.filter(user = the_connected_user)[0]


        mail_type_object = MailType.objects.filter(id=mail_type)
        sender_object = Sender.objects.filter(id=sender)

        if len(mail_type_object) > 0:
            mail_type_object = mail_type_object[0]
        if len(sender_object) > 0:
            sender_object = sender_object[0]

        existing_mail = Mail.objects.filter(number = internal_number)
        if len(existing_mail) > 0:
            message_to_user = "Error. A mail with number '"+internal_number+"' already exists. Use an other number"
            d["pagetitle"] = "New mails"
            d["mail_types"] = MailType.objects.all()
            d["senders"] = Sender.objects.all().order_by("first_name")
            d["mails"] = (Mail.objects.filter(track = None)
                .annotate(sender_f_name = F('sender__first_name'))
                .annotate(sender_l_name = F('sender__last_name'))
                .annotate(mail_type_name = F('mail_type__mail_type_name'))
                )
            d["mails"] = d["mails"].values()
            d["mails"] = json.dumps(list(d["mails"]), default=date_handler)
            d["message_to_user"] = message_to_user
            return render(request, 'new_mail_1.html', d)
        else:
            if soft_copy:
                created_mail = Mail.objects.create(
                    external_number = external_number, 
                    number = internal_number, sender = sender_object, 
                    mail_type = mail_type_object, 
                    need_answer = the_answer_is_needed, 
                    received_time = reception_date_time, 
                    soft_copy = soft_copy
                    )
                Track.objects.create(
                    mail = created_mail,
                    staff = the_connected_staff,
                    hard_copy_transfer_time = reception_date_time,
                    purpose = "For ventation",
                    soft_copy = soft_copy
                )
            else:
                created_mail = Mail.objects.create(
                    external_number = external_number, 
                    number = internal_number, sender = sender_object, 
                    mail_type = mail_type_object, 
                    need_answer = the_answer_is_needed, 
                    received_time = reception_date_time, 
                    )
                Track.objects.create(
                    mail = created_mail,
                    staff = the_connected_staff,
                    hard_copy_transfer_time = reception_date_time,
                    purpose = "For ventation",
                )

    d["pagetitle"] = "New mails"
    d["mail_types"] = MailType.objects.all()
    d["senders"] = Sender.objects.all().order_by("first_name")
    d["mails"] = (Mail.objects.filter(track = None)
        .annotate(sender_f_name = F('sender__first_name'))
        .annotate(sender_l_name = F('sender__last_name'))
        .annotate(mail_type_name = F('mail_type__mail_type_name'))
        )
    d["mails"] = d["mails"].values()
    d["mails"] = json.dumps(list(d["mails"]), default=date_handler)
    d["message_to_user"] = message_to_user
    return render(request, 'new_mail_1.html', d)


def partners(request):
    d = {}
    message_to_user = ""
    if request.method == 'POST':
        first_mame = request.POST.get('first_mame')
        last_name = request.POST.get('last_name')
        first_mame = unicodedata.normalize('NFKD', first_mame).encode('ascii','ignore')
        last_name = unicodedata.normalize('NFKD', last_name).encode('ascii','ignore')
        if(len(first_mame) < 1):
            message_to_user = "Error. First Name field can not be empty"
            d["message_to_user"] = message_to_user
            senders = Sender.objects.all().order_by("first_name").values()
            d["senders"] = json.dumps(list(senders), default=date_handler)
            return render(request, 'partners.html', d)
        else:
            first_mame = first_mame.upper()

        if(len(last_name) > 0):
            last_name = last_name.upper()

        Sender.objects.create(first_name = first_mame, last_name = last_name)
    senders = Sender.objects.all().order_by("first_name").values()
    d["senders"] = json.dumps(list(senders), default=date_handler)
    d["message_to_user"] = message_to_user
    return render(request, 'partners.html', d)

def close_mail_view(request):
    d = {}
    d["senders"] = Sender.objects.all().order_by("first_name")
    d["unclosed_mails"] = Mail.objects.filter(closed = False)
    d["closed_mails"] = Mail.objects.filter(closed = True)
    return render(request, 'close.html', d)

def mail_details(request, mail_number):
    d = {}
    mail_number = str(request.GET.get('mail_number', '')).strip()

    one_mail_follow_up_data = (Track.objects.filter(mail__number = mail_number)
        .values("staff__section__designation")
        .annotate(processing_time_in_section=Sum(F('end_date')-F('start_date'))))

    for one_section in one_mail_follow_up_data:
        if one_section["processing_time_in_section"]:
            one_section["processing_time_in_section"] = one_section["processing_time_in_section"].total_seconds()
        else:
            one_section["processing_time_in_section"] = 0

    d["pie_chart_by_sections"] = one_mail_follow_up_data
    return render(request, 'mail_details.html', d)


def stat_all_mails(request):
    d = {}
    all_pie_data = Mail.objects.all().values("closed").annotate(number=Count('closed'))
    d["number_of_all_mails"] = Mail.objects.all().count()
    d["all_pie_data"] = all_pie_data

    d["mails"] = Mail.objects.all().annotate(sender_f_name = F('sender__first_name')).annotate(sender_l_name = F('sender__last_name')).annotate(mail_type_name = F('mail_type__mail_type_name'))
    d["mails"] = d["mails"].values()
    d["mails"] = json.dumps(list(d["mails"]), default=date_handler)


    return render(request, 'stat_all_mails.html', d)

def stat_closed_mails(request):
    d = {}
    closed_pie_data = (Mail.objects.filter(closed = "True")
        .annotate(processing_time=DiffDays(CastDate(F('closed_time'))-CastDate(F('received_time'))) + 1)
        .values('processing_time')
        .annotate(number_same_time=Count('processing_time')))
    d["number_of_completed_mails"] = Mail.objects.filter(closed = "True").count()
    d["closed_pie_data"] = closed_pie_data
    return render(request, 'stat_closed_mails.html', d)

def stat_not_closed_mails(request):
    d = {}
    current_date = datetime.datetime.now().date()

    not_closed_pie_data = (Mail.objects.filter(closed = False)
        .annotate(processing_time=DiffDays(CastDate(current_date)-CastDate(F('received_time'))) + 1)
        .values('processing_time')
        .annotate(number_same_time=Count('processing_time')))
    d["number_of_not_completed_mails"] = Mail.objects.filter(closed = "False").count()
    d["not_closed_pie_data"] = not_closed_pie_data.order_by('processing_time')


    '''not_closed_pie_data_2 = (Track.objects.select_related()
        .filter(end_date__isnull=True, mail__closed = False)
        .annotate(received_date=F('mail__received_time'))
        .annotate(need_answer=F('mail__need_answer'))
        .annotate(staff_f_name=F('staff__first_name'))
        .annotate(staff_l_name=F('staff__last_name'))
        .annotate(staff_section=F('staff__section__designation'))
        .values('staff_section')
        .annotate(number_of_mails_in_section=Count('staff_section')))'''
    not_closed_pie_data_2 = (Track.objects.select_related()
        .filter(mail__closed = False)
        .annotate(max_date = Max("mail__track__start_date"))
        .filter(start_date = F('max_date'))
        .annotate(received_date=F('mail__received_time'))
        .annotate(need_answer=F('mail__need_answer'))
        .annotate(staff_f_name=F('staff__first_name'))
        .annotate(staff_l_name=F('staff__last_name'))
        .annotate(staff_section=F('staff__section__designation'))
        .values('staff_section')
        .annotate(number_of_mails_in_section=Count('staff_section')))
    d["not_closed_pie_data_2"] = not_closed_pie_data_2



    '''not_closed_pie_data_3 = (Track.objects.select_related()
        .filter(end_date__isnull=True, mail__closed = False)
        .annotate(received_date=F('mail__received_time'))
        .annotate(staff_f_name=F('staff__first_name'))
        .annotate(staff_l_name=F('staff__last_name'))
        .annotate(staff_section=F('staff__section__designation'))
        .values('staff__id', 'staff__first_name', 'staff__last_name', 'staff__section__designation')
        .annotate(number_of_mails_for_one_staff=Count('staff__first_name')))'''
    '''not_closed_pie_data_3 = (Track.objects.select_related()
        .filter(mail__closed = False)
        .annotate(max_date = Max("mail__track__start_date"))
        .filter(start_date = F('max_date'))
        .annotate(received_date=F('mail__received_time'))
        .annotate(staff_f_name=F('staff__first_name'))
        .annotate(staff_l_name=F('staff__last_name'))
        .annotate(staff_section=F('staff__section__designation'))
        .values('staff__id', 'staff__first_name', 'staff__last_name', 'staff__section__designation')
        .annotate(number_of_mails_for_one_staff=Count('staff__first_name')))
    d["not_closed_pie_data_3"] = not_closed_pie_data_3'''
    not_closed_pie_data_3 = Track.objects.filter(mail__closed = False).annotate(max_date = Max("mail__track__start_date")).values('staff__id', 'staff__first_name', 'staff__last_name', 'staff__section__designation').annotate(number_of_mails_for_one_staff=Count('staff__first_name'))
    d["not_closed_pie_data_3"] = not_closed_pie_data_3
    



    not_closed_mails = (Mail.objects.filter(closed = False)
        .annotate(sender_f_name = F('sender__first_name'))
        .annotate(sender_l_name = F('sender__last_name'))
        .annotate(mail_type_name = F('mail_type__mail_type_name'))
        ).values()
    d['not_closed_mails'] = json.dumps(list(not_closed_mails), default=date_handler)



    '''not_closed_mails_2 = (Track.objects.select_related()
        .filter(end_date__isnull=True, mail__closed = False)
        .annotate(mail_internal_number=F('mail__number'))
        .annotate(mail_type=F('mail__mail_type__mail_type_name'))
        .annotate(recorded_date=F('mail__received_time'))
        .annotate(sender_f_name = F('mail__sender__first_name'))
        .annotate(sender_l_name = F('mail__sender__last_name'))
        .annotate(need_answer=F('mail__need_answer'))
        .annotate(staff_f_name=F('staff__first_name'))
        .annotate(staff_l_name=F('staff__last_name'))
        .annotate(staff_section=F('staff__section__designation'))
        .annotate(number_of_days_in_the_system=DiffDays(CastDate(current_date)-CastDate(F('mail__received_time'))) + 1)
        ).values()'''
    not_closed_mails_2 = (Track.objects.select_related()
        .filter(mail__closed = False)
        .annotate(max_date = Max("mail__track__start_date"))
        .filter(start_date = F('max_date'))
        .annotate(mail_internal_number=F('mail__number'))
        .annotate(mail_type=F('mail__mail_type__mail_type_name'))
        .annotate(recorded_date=F('mail__received_time'))
        .annotate(sender_f_name = F('mail__sender__first_name'))
        .annotate(sender_l_name = F('mail__sender__last_name'))
        .annotate(need_answer=F('mail__need_answer'))
        .annotate(staff_f_name=F('staff__first_name'))
        .annotate(staff_l_name=F('staff__last_name'))
        .annotate(staff_section=F('staff__section__designation'))
        .annotate(number_of_days_in_the_system=DiffDays(CastDate(current_date)-CastDate(F('mail__received_time'))) + 1)
        ).values()
    d['not_closed_mails_2'] = json.dumps(list(not_closed_mails_2), default=date_handler)


    return render(request, 'stat_not_closed_mails.html', d)


def save_mail(request):
    response_data = {}
    if request.method == 'POST':
        #import pdb; pdb.set_trace()
        json_data = json.loads(request.body)
        mail_type = json_data['mail_type']
        sender = json_data['sender']
        mail_number = json_data['mail_number']
        external_mail_number = json_data['external_mail_number']
        
        mail_type_object = MailType.objects.filter(id=mail_type)
        sender_object = Sender.objects.filter(id=sender)

        if len(mail_type_object) > 0:
            mail_type_object = mail_type_object[0]
        if len(sender_object) > 0:
            sender_object = sender_object[0]

        existing_mail = Mail.objects.filter(number = mail_number)
        if len(existing_mail) > 0:
            print "Error. A record with that number already exists."
        else:
            Mail.objects.create(external_number = external_mail_number, number = mail_number, sender = sender_object, mail_type = mail_type_object)

        return HttpResponse(response_data, content_type="application/json")


def save_mail_1(request):
    response_data = {}
    if request.method == 'POST':
        #import pdb; pdb.set_trace()
        #json_data = json.loads(request.body)
        json_data = json.loads(request.POST['json_data'])
        soft_copy = request.POST['soft_copy']

        mail_type = json_data['mail_type']
        sender = json_data['sender']
        mail_number = json_data['mail_number']
        answer_needed = json_data['answerNeeded']
        external_mail_number = json_data['external_mail_number']
        datetimepicked = json_data['datetimepicked']
        date_time_picked = datetime.datetime.strptime(datetimepicked, '%m/%d/%Y %I:%M %p')

        soft_copy_fake_url = (
            unicodedata.normalize('NFKD', soft_copy_fake_url)
            .encode('ascii','ignore')
            )
        soft_copy_fake_url = soft_copy_fake_url.split("\\")
        soft_copy = soft_copy_fake_url[2]


        mail_type_object = MailType.objects.filter(id=mail_type)
        sender_object = Sender.objects.filter(id=sender)

        if len(mail_type_object) > 0:
            mail_type_object = mail_type_object[0]
        if len(sender_object) > 0:
            sender_object = sender_object[0]

        existing_mail = Mail.objects.filter(number = mail_number)
        if len(existing_mail) > 0:
            print "Error. A record with that number already exists."
        else:
            Mail.objects.create(
                external_number = external_mail_number, 
                number = mail_number, sender = sender_object, 
                mail_type = mail_type_object, 
                need_answer = answer_needed, 
                received_time = date_time_picked, 
                #soft_copy = soft_copy
                )
        
        return HttpResponse(response_data, content_type="application/json")


def transfer_mail(request):
    d = {}
    d["senders"] = Sender.objects.all()
    d["staff"] = Staff.objects.all().annotate(section_name = F('section__designation'))
    d["transfers"] = (Track.objects.filter(end_date__isnull = True)
        .annotate(sender_f_name = F('mail__sender__first_name'))
        .annotate(sender_l_name = F('mail__sender__last_name'))
        .annotate(mail_number = F('mail__number'))
        .annotate(staff_f_name = F('staff__first_name'))
        .annotate(staff_l_name = F('staff__last_name'))
        .annotate(section = F('staff__section__designation'))
        )
    d["transfers"] = d["transfers"].values()
    d["transfers"] = json.dumps(list(d["transfers"]), default=date_handler)
    return render(request, 'transfer.html', d)


def transfer_mail_1(request):
    d = {}
    if request.method == 'POST':
        sender = request.POST.get('sender')
        mail = request.POST.get('mail')
        staff = request.POST.get('staff')
        hard_copy_transfer_date = request.POST.get('hard_copy_transfer_date')
        comments = request.POST.get('comments')
        comments = comments.strip()
        soft_copy = request.FILES['soft_copy'] if 'soft_copy' in request.FILES else False

        #If datetime about when a soft copy has been uploaded is not available, we consider 
        #the current datetime
        if hard_copy_transfer_date:
            hard_copy_transfer_date = datetime.datetime.strptime(hard_copy_transfer_date, '%m/%d/%Y %I:%M %p')
        else:
            hard_copy_transfer_date = datetime.datetime.now()

        task_end_date = datetime.datetime.now()

        sender_record = Sender.objects.filter(id=sender)
        mail_record = Mail.objects.filter(number=mail)
        staff_record = Staff.objects.filter(id=staff)

        if len(sender_record) > 0:
            sender_record = sender_record[0]
        if len(mail_record) > 0:
            mail_record = mail_record[0]
        if len(staff_record) > 0:
            staff_record = staff_record[0]


        mail_related_track_records = Track.objects.filter(mail = mail_record).order_by("id")
        last = mail_related_track_records[len(mail_related_track_records) - 1] if mail_related_track_records else None


        if last is not None:
            #last.end_date = hard_copy_transfer_date
            last.end_date = task_end_date
            last.save()
            if last.staff != staff_record:
                #We can not transfer a mail to someone if it is already there
                #If a soft copy is not uploaded, we consider the last related soft copy if it is available
                soft_copy_available = False
                if not soft_copy:
                    last_mails_record_with_soft_copy = Track.objects.filter(mail = mail_record, soft_copy__isnull = False).order_by("-id")
                    if(len(last_mails_record_with_soft_copy) < 1):
                        last_mails_record_with_soft_copy = Mail.objects.filter(number = mail, soft_copy__isnull = False)
                    if(len(last_mails_record_with_soft_copy) > 0):
                        soft_copy_available = True
                        soft_copy = last_mails_record_with_soft_copy[0].soft_copy
                else:
                    soft_copy_available = True

                if soft_copy_available:
                    Track.objects.create(
                        mail = mail_record,
                        staff = staff_record,
                        hard_copy_transfer_time = hard_copy_transfer_date,
                        purpose = comments,
                        soft_copy = soft_copy
                        )
                else:
                    Track.objects.create(
                        mail = mail_record, 
                        staff = staff_record, 
                        hard_copy_transfer_time = hard_copy_transfer_date, 
                        purpose = comments
                        )

                mail_external_number = mail_record.external_number
                mail_internal_number = mail_record.number

                e_mail_body = ("Dear "+staff_record.first_name+", "+
                    "a mail with "+mail_external_number+" as external number "+
                    "and "+mail_internal_number+" as internal number "+
                    "has been sent to you for processing. "+
                    "Best regards.")

                e_mail_subject = "Push and Track - A mail has been sent to you for processing"

                e_mail_sender = "noreply@pushandtrack.org"

                e_mail_receiver = staff_record.user.email

                tranfer_staff_email = request.user.email

                send_mail(e_mail_subject, e_mail_body, e_mail_sender, [e_mail_receiver, tranfer_staff_email,])
            else:
                #Write here a code you want to be executed if staff A is trying to transfer a mail 
                #to staff B while the mail is already to staff B
                pass

    the_connected_user = request.user
    d["senders"] = Sender.objects.all().order_by("first_name")
    d["staff"] = Staff.objects.all().annotate(section_name = F('section__designation')).order_by("section_name")
    
    '''d["transfers"] = (Track.objects.filter(end_date__isnull = True, mail__closed = False , staff__user = the_connected_user)
        .annotate(sender_f_name = F('mail__sender__first_name'))
        .annotate(sender_l_name = F('mail__sender__last_name'))
        .annotate(mail_number = F('mail__number'))
        .annotate(staff_f_name = F('staff__first_name'))
        .annotate(staff_l_name = F('staff__last_name'))
        .annotate(section = F('staff__section__designation'))
        )'''

    '''d["transfers"] = (Mail.objects.filter(closed = False)
        .annotate(max_date = Max("track__start_date"))
        .filter(track__staff__user = the_connected_user, track__start_date = F('max_date'))
        .annotate(sender_f_name = F('track__mail__sender__first_name'))
        .annotate(sender_l_name = F('track__mail__sender__last_name'))
        .annotate(mail_number = F('track__mail__number'))
        .annotate(staff_f_name = F('track__staff__first_name'))
        .annotate(staff_l_name = F('track__staff__last_name'))
        .annotate(section = F('track__staff__section__designation'))
        .annotate(hard_copy_transfer_time = F('track__hard_copy_transfer_time'))
        .annotate(purpose = F('track__purpose'))
        .annotate(start_date = F('track__start_date'))
        )'''

    d["transfers"] = (Track.objects.filter(mail__closed = False)
        .annotate(max_date = Max("mail__track__start_date"))
        .filter(staff__user = the_connected_user, start_date = F('max_date'))
        .annotate(sender_f_name = F('mail__sender__first_name'))
        .annotate(sender_l_name = F('mail__sender__last_name'))
        .annotate(mail_number = F('mail__number'))
        .annotate(staff_f_name = F('staff__first_name'))
        .annotate(staff_l_name = F('staff__last_name'))
        .annotate(section = F('staff__section__designation'))
        )

    d["transfers"] = d["transfers"].values()

    d["transfers"] = json.dumps(list(d["transfers"]), default=date_handler)
    return render(request, 'transfer_1.html', d)


def save_transfer(request):
    response_data = {}
    if request.method == 'POST':
        #import pdb; pdb.set_trace()
        json_data = json.loads(request.body)
        sender = int(json_data['sender'])
        mail = json_data['mail']
        staff = json_data['staff']
        comments = json_data['comments']

        sender_record = Sender.objects.filter(id=sender)
        mail_record = Mail.objects.filter(number=mail)
        staff_record = Staff.objects.filter(id=staff)

        if len(sender_record) > 0:
            sender_record = sender_record[0]
        if len(mail_record) > 0:
            mail_record = mail_record[0]
        if len(staff_record) > 0:
            staff_record = staff_record[0]
        # Let's first record that the staff who is transfering this mail finished his work
        mail_related_track_records = Track.objects.filter(mail = mail_record)
        last = mail_related_track_records[len(mail_related_track_records) - 1] if mail_related_track_records else None
        if last is not None:
            last.end_date = datetime.datetime.now()
            last.save()
        else:
            pass
        Track.objects.create(mail = mail_record, staff = staff_record, purpose = comments)
        return HttpResponse(response_data, content_type="application/json")


def save_transfer_1(request):
    response_data = {}
    if request.method == 'POST':
        #import pdb; pdb.set_trace()
        json_data = json.loads(request.body)
        sender = int(json_data['sender'])
        mail = json_data['mail']
        staff = json_data['staff']
        datetimepicked = json_data['hard_copy_transfer_date']
        hard_copy_transfer_date = datetime.datetime.strptime(datetimepicked, '%m/%d/%Y %I:%M %p')
        comments = json_data['comments']

        sender_record = Sender.objects.filter(id=sender)
        mail_record = Mail.objects.filter(number=mail)
        staff_record = Staff.objects.filter(id=staff)

        if len(sender_record) > 0:
            sender_record = sender_record[0]
        if len(mail_record) > 0:
            mail_record = mail_record[0]
        if len(staff_record) > 0:
            staff_record = staff_record[0]
        mail_related_track_records = Track.objects.filter(mail = mail_record)
        last = mail_related_track_records[len(mail_related_track_records) - 1] if mail_related_track_records else None
        if last is not None:
            #last.end_date = datetime.datetime.now()
            last.end_date = hard_copy_transfer_date
            last.save()
        else:
            pass

        Track.objects.create(
            mail = mail_record, 
            staff = staff_record, 
            hard_copy_transfer_time = hard_copy_transfer_date, 
            purpose = comments
            )
        mail_external_number = mail_record.external_number
        mail_internal_number = mail_record.number

        e_mail_body = ("Dear "+staff_record.first_name+", "+
            "a mail with "+mail_external_number+" as external number "+
            "and "+mail_internal_number+" as internal number "+
            "has been sent to you for processing. "+
            "Best regards.")

        e_mail_subject = "Push and Track - A mail has been sent to you for processing"

        e_mail_sender = "noreply@pushandtrack.org"

        e_mail_receiver = staff_record.user.email

        tranfer_staff_email = request.user.email

        send_mail(e_mail_subject, e_mail_body, e_mail_sender, [e_mail_receiver, tranfer_staff_email,])

        return HttpResponse(response_data, content_type="application/json")

def track_mails(request):
    d = {}
    d["pagetitle"] = "Track mails"
    return render(request, 'track_mails.html', d)

def search_mail(request):
    mail_history = ""
    if request.method == 'POST':
        json_data = json.loads(request.body)
        mail_id = json_data['mail_id']
        mail_id = mail_id.strip()
        concerned_mail = Mail.objects.filter(~Q(track = None), number__contains = mail_id)
        if(len(concerned_mail) > 0):
            first = True
            for one_mail in concerned_mail:
                sender = one_mail.sender
                received_time = one_mail.received_time
                one_mail_history = (
                    Track.objects.filter(mail = one_mail).order_by('start_date')
                    .annotate(received_date=F('mail__received_time'))
                    .annotate(internal_number=F('mail__number'))
                    .annotate(external_number=F('mail__external_number'))
                    .annotate(sender_f_name = F('mail__sender__first_name'))
                    .annotate(sender_l_name = F('mail__sender__last_name'))
                    .annotate(staff_f_name=F('staff__first_name'))
                    .annotate(staff_l_name=F('staff__last_name'))
                    .annotate(staff_section=F('staff__section__designation'))
                )
                #one_mail_history = mail_history.values()
                if first == True:
                    mail_history = one_mail_history
                    first = False
                else:
                    mail_history = mail_history | one_mail_history
            mail_history = mail_history.values()
        else:
            mail_history = "N"
        mail_history = json.dumps(list(mail_history), default=date_handler)
    return HttpResponse(mail_history, content_type="application/json")


def close_mail(request):
    response_data = {}
    if request.method == 'POST':
        json_data = json.loads(request.body)
        sender = int(json_data['sender'])
        mail = json_data['mail']
        the_mail = Mail.objects.filter(number = mail)
        if len(the_mail) > 0:
            the_mail = the_mail[0]
            the_mail.closed = True
            the_mail.closed_time = datetime.datetime.now()
            the_mail.save()

            # Let's first record that the staff who was working on this mail finished his work
            mail_related_track_records = Track.objects.filter(mail = the_mail)
            last = mail_related_track_records[len(mail_related_track_records) - 1] if mail_related_track_records else None
            if last is not None:
                last.end_date = datetime.datetime.now()
                last.save()
            else:
                pass
    return HttpResponse(response_data, content_type="application/json")

def get_unclosed_mails(request):
    response_data = {}
    if request.method == 'POST':
        json_data = json.loads(request.body)
        sender_id = json_data['code']
        sender = Sender.objects.filter(id=sender_id)
        if len(sender) > 0:
            sender = sender[0]
            the_connected_user = request.user
            if(the_connected_user.groups.filter(name__in = ['Receptionist']).exists()):
                '''mails = (Track.objects.filter(end_date__isnull = True, 
                    mail__sender = sender)
                    .annotate(sender_f_name = F('mail__sender__first_name'))
                    .annotate(sender_l_name = F('mail__sender__last_name'))
                    .annotate(number = F('mail__number'))
                    .annotate(staff_f_name = F('staff__first_name'))
                    .annotate(staff_l_name = F('staff__last_name'))
                    .annotate(section = F('staff__section__designation'))
                    )'''
                mails = (Track.objects.filter(mail__closed = False, mail__sender = sender)
                    .annotate(max_date = Max("mail__track__start_date"))
                    .filter(start_date = F('max_date'))
                    .annotate(sender_f_name = F('mail__sender__first_name'))
                    .annotate(sender_l_name = F('mail__sender__last_name'))
                    .annotate(number = F('mail__number'))
                    .annotate(staff_f_name = F('staff__first_name'))
                    .annotate(staff_l_name = F('staff__last_name'))
                    .annotate(section = F('staff__section__designation'))
                    )
            else:
                '''mails = (Track.objects.filter(end_date__isnull = True, 
                    staff__user = the_connected_user, 
                    mail__sender = sender)
                    .annotate(sender_f_name = F('mail__sender__first_name'))
                    .annotate(sender_l_name = F('mail__sender__last_name'))
                    .annotate(number = F('mail__number'))
                    .annotate(staff_f_name = F('staff__first_name'))
                    .annotate(staff_l_name = F('staff__last_name'))
                    .annotate(section = F('staff__section__designation'))
                    )'''
                mails = (Track.objects.filter(mail__closed = False, mail__sender = sender)
                    .annotate(max_date = Max("mail__track__start_date"))
                    .filter(staff__user = the_connected_user, start_date = F('max_date'))
                    .annotate(sender_f_name = F('mail__sender__first_name'))
                    .annotate(sender_l_name = F('mail__sender__last_name'))
                    .annotate(number = F('mail__number'))
                    .annotate(staff_f_name = F('staff__first_name'))
                    .annotate(staff_l_name = F('staff__last_name'))
                    .annotate(section = F('staff__section__designation'))
                    )
            mails = mails.values()
            mails = json.dumps(list(mails), default=date_handler)

    return HttpResponse(mails, content_type="application/json")


def get_closed_mails(request):
    response_data = {}
    if request.method == 'POST':
        json_data = json.loads(request.body)
        sender_id = json_data['code']
        sender = Sender.objects.filter(id=sender_id)
        if len(sender) > 0:
            sender = sender[0]
            mails = Mail.objects.filter(sender = sender, closed = True)
            '''response_data["mails"] = mails'''
            mails = mails.values()
            mails = json.dumps(list(mails), default=date_handler)
            mails = json.loads(mails)
            mails = json.dumps(mails, default=date_handler)


    return HttpResponse(mails, content_type="application/json")


def get_on_process_mails_for_staff(request, staff_id):
    mails_under_processing = {}
    staff_id = int(request.GET.get("staff_id", ""))
    mails_under_processing["mails"] = (Track.objects.select_related()
        .filter(end_date__isnull=True, mail__closed = False, staff__id = staff_id)
        .annotate(received_by_organization_date=F('mail__received_time'))
        .annotate(sender_f_name=F('mail__sender__first_name'))
        .annotate(sender_l_name=F('mail__sender__last_name'))
        .annotate(mail_number=F('mail__number')))
    mails_under_processing["mails"] = mails_under_processing["mails"].values()
    mails_under_processing["mails"] = json.dumps(list(mails_under_processing["mails"]), default=date_handler)
    return render(request, "on_process_mails_for_staff.html", mails_under_processing)






class MailListView(SingleTableView):
    model = Mail
    table_pagination = False
    mails_table = MailTable
    template_name = 'all_mails.html'


class MailTypeListView(SingleTableView):
    model = MailType
    table_pagination = False
    mail_type_table = MailTypeTable
    template_name = 'all_mail_types.html'

class SectionListView(SingleTableView):
    model = Section
    table_pagination = False
    section_table = SectionTable
    template_name = 'all_sections.html'


class SenderListView(SingleTableView):
    model = Sender
    table_pagination = False
    sender_table = SenderTable
    template_name = 'all_senders.html'


class StaffPositionListView(SingleTableView):
    model = StaffPosition
    table_pagination = False
    staff_position_table = StaffPosition
    template_name = 'all_staff_positions.html'

class StaffListView(SingleTableView):
    model = Staff
    table_pagination = False
    staff_table = StaffTable
    template_name = 'all_staffs.html'

class TrackListView(SingleTableView):
    model = Track
    table_pagination = False
    track_table = TrackTable
    template_name = 'all_tracks.html'
