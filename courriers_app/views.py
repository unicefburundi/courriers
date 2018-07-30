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
    print "BBB"
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


def track_mail(request):
    d = {}
    return render(request, 'track_mail.html', d)
