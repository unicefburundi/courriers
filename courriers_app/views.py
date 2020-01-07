# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from courriers_app.models import *
from forms import *
from django.http import HttpResponse
import json
from django.db.models import F, Count, Func, Sum
import datetime
from django.core import serializers
import unicodedata
from django.core.mail import send_mail


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
    return render(request, 'new_mail_1.html', d)

def close_mail_view(request):
    d = {}
    d["senders"] = Sender.objects.all()
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
            one_section["processing_time_in_section"] = int(one_section["processing_time_in_section"].total_seconds()) / 60
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

    not_closed_pie_data = (Mail.objects.filter(closed = "False")
        .annotate(processing_time=DiffDays(CastDate(current_date)-CastDate(F('received_time'))) + 1)
        .values('processing_time')
        .annotate(number_same_time=Count('processing_time')))
    d["number_of_not_completed_mails"] = Mail.objects.filter(closed = "False").count()
    d["not_closed_pie_data"] = not_closed_pie_data

    not_closed_pie_data_2 = (Track.objects.select_related()
        .filter(end_date__isnull=True, mail__closed = "False")
        .annotate(received_date=F('mail__received_time'))
        .annotate(staff_f_name=F('staff__first_name'))
        .annotate(staff_l_name=F('staff__last_name'))
        .annotate(staff_section=F('staff__section__designation'))
        .values('staff_section')
        .annotate(number_of_mails_in_section=Count('staff_section')))
    d["not_closed_pie_data_2"] = not_closed_pie_data_2

    not_closed_pie_data_3 = (Track.objects.select_related()
        .filter(end_date__isnull=True, mail__closed = "False")
        .annotate(received_date=F('mail__received_time'))
        .annotate(staff_f_name=F('staff__first_name'))
        .annotate(staff_l_name=F('staff__last_name'))
        .annotate(staff_section=F('staff__section__designation'))
        .values('staff__id', 'staff__first_name', 'staff__last_name', 'staff__section__designation')
        .annotate(number_of_mails_for_one_staff=Count('staff__first_name')))
    d["not_closed_pie_data_3"] = not_closed_pie_data_3

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
        json_data = json.loads(request.body)
        mail_type = json_data['mail_type']
        sender = json_data['sender']
        mail_number = json_data['mail_number']
        answer_is_needed = json_data['answerNeeded']
        external_mail_number = json_data['external_mail_number']
        datetimepicked = json_data['datetimepicked']
        date_time_picked = datetime.datetime.strptime(datetimepicked, '%m/%d/%Y %I:%M %p')
        #soft_copy_fake_url = json_data['softCopy']
        '''soft_copy_fake_url = (
            unicodedata.normalize('NFKD', soft_copy_fake_url)
            .encode('ascii','ignore')
            )
        soft_copy_fake_url = soft_copy_fake_url.split("\\")
        soft_copy = soft_copy_fake_url[2]'''
        if answer_is_needed:
            answer_needed = True
        else:
            answer_needed = False

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
        concerned_mail = Mail.objects.filter(number = mail_id)
        if(len(concerned_mail) > 0):
            concerned_mail = concerned_mail[0]
            sender = concerned_mail.sender
            received_time = concerned_mail.received_time
            mail_history = (
                Track.objects.filter(mail = concerned_mail)
                .annotate(received_date=F('mail__received_time'))
                .annotate(staff_f_name=F('staff__first_name'))
                .annotate(staff_l_name=F('staff__last_name'))
                .annotate(staff_section=F('staff__section__designation'))
                )
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
            mails = Mail.objects.filter(sender = sender, closed = False)
            '''response_data["mails"] = mails'''
            mails = mails.values()
            mails = json.dumps(list(mails), default=date_handler)
            mails = json.loads(mails)
            mails = json.dumps(mails, default=date_handler)


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
        .filter(end_date__isnull=True, mail__closed = "False", staff__id = staff_id)
        .annotate(received_by_organization_date=F('mail__received_time'))
        .annotate(sender_f_name=F('mail__sender__first_name'))
        .annotate(sender_l_name=F('mail__sender__last_name'))
        .annotate(mail_number=F('mail__number')))
    mails_under_processing["mails"] = mails_under_processing["mails"].values()
    mails_under_processing["mails"] = json.dumps(list(mails_under_processing["mails"]), default=date_handler)
    return render(request, "on_process_mails_for_staff.html", mails_under_processing)