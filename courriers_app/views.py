# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from courriers_app.models import *
from forms import *
from django.http import HttpResponse
import json
from django.db.models import F, Count, Func
import datetime
from django.core import serializers


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
    d["mails"] = Mail.objects.all().annotate(sender_f_name = F('sender__first_name')).annotate(sender_l_name = F('sender__last_name')).annotate(mail_type_name = F('mail_type__mail_type_name'))
    d["mails"] = d["mails"].values()
    d["mails"] = json.dumps(list(d["mails"]), default=date_handler)
    return render(request, 'new_mail.html', d)

def close_mail_view(request):
    d = {}
    d["senders"] = Sender.objects.all()
    d["unclosed_mails"] = Mail.objects.filter(closed = False)
    d["closed_mails"] = Mail.objects.filter(closed = True)
    return render(request, 'close.html', d)


def stat_all_mails(request):
    d = {}
    all_pie_data = Mail.objects.all().values("closed").annotate(number=Count('closed'))
    d["number_of_all_mails"] = Mail.objects.all().count()
    d["all_pie_data"] = all_pie_data

    return render(request, 'stat_all_mails.html', d)

def stat_closed_mails(request):
    d = {}
    closed_pie_data = Mail.objects.filter(closed = "True").annotate(processing_time=DiffDays(CastDate(F('closed_time'))-CastDate(F('received_time'))) + 1).values('processing_time').annotate(number_same_time=Count('processing_time'))
    d["number_of_completed_mails"] = Mail.objects.filter(closed = "True").count()
    d["closed_pie_data"] = closed_pie_data
    return render(request, 'stat_closed_mails.html', d)

def stat_not_closed_mails(request):
    d = {}
    current_date = datetime.datetime.now().date()

    not_closed_pie_data = Mail.objects.filter(closed = "False").annotate(processing_time=DiffDays(CastDate(current_date)-CastDate(F('received_time'))) + 1).values('processing_time').annotate(number_same_time=Count('processing_time'))
    d["number_of_not_completed_mails"] = Mail.objects.filter(closed = "False").count()
    d["not_closed_pie_data"] = not_closed_pie_data

    not_closed_pie_data_2 = Track.objects.select_related().filter(end_date__isnull=True, mail__closed = "False").annotate(received_date=F('mail__received_time')).annotate(staff_f_name=F('staff__first_name')).annotate(staff_l_name=F('staff__last_name')).annotate(staff_section=F('staff__section__designation')).values('staff_section').annotate(number_of_mails_in_section=Count('staff_section'))
    d["not_closed_pie_data_2"] = not_closed_pie_data_2
    
    

    return render(request, 'stat_not_closed_mails.html', d)


def save_mail(request):
    response_data = {}
    if request.method == 'POST':
        #import pdb; pdb.set_trace()
        json_data = json.loads(request.body)
        mail_type = json_data['mail_type']
        sender = json_data['sender']
        mail_number = json_data['mail_number']
        
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
            Mail.objects.create(number = mail_number, sender = sender_object, mail_type = mail_type_object)

        return HttpResponse(response_data, content_type="application/json")

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


        Track.objects.create(mail = mail_record, staff = staff_record, purpose = comments)

        return HttpResponse(response_data, content_type="application/json")


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
    return HttpResponse(response_data, content_type="application/json")

def transfer_mail(request):
    d = {}
    d["senders"] = Sender.objects.all()
    d["staff"] = Staff.objects.all().annotate(section_name = F('section__designation'))
    d["transfers"] = Track.objects.all().annotate(sender_f_name = F('mail__sender__first_name')).annotate(sender_l_name = F('mail__sender__last_name')).annotate(mail_number = F('mail__number')).annotate(staff_f_name = F('staff__first_name')).annotate(staff_l_name = F('staff__last_name')).annotate(section = F('staff__section__designation'))
    d["transfers"] = d["transfers"].values()
    d["transfers"] = json.dumps(list(d["transfers"]), default=date_handler)
    return render(request, 'transfer.html', d)

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

