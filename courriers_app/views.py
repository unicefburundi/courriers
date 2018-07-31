# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from courriers_app.models import *
from forms import *
from django.http import HttpResponse
import json
from django.db.models import F


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
    '''if request.method == 'POST' and request.FILES['my_file']:'''
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

        track.objects.create(mail = mail_record, staff = staff_record, purpose = comments)

        return HttpResponse(response_data, content_type="application/json")


def transfer_mail(request):
    d = {}
    d["senders"] = Sender.objects.all()
    d["staff"] = Staff.objects.all().annotate(section_name = F('section__designation'))
    return render(request, 'transfer.html', d)

def get_mails(request):
    response_data = {}
    if request.method == 'POST':
        json_data = json.loads(request.body)
        sender_id = json_data['code']
        sender = Sender.objects.filter(id=sender_id)
        if len(sender) > 0:
            sender = sender[0]
            mails = Mail.objects.filter(sender = sender)
            '''response_data["mails"] = mails'''
            mails = mails.values()
            mails = json.dumps(list(mails), default=date_handler)
            mails = json.loads(mails)
            mails = json.dumps(mails, default=date_handler)

            print mails
    '''return HttpResponse(response_data)
    '''     
    print(mails)
    return HttpResponse(mails, content_type="application/json")

