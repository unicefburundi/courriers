# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from courriers_app.models import *
from forms import *
from django.http import HttpResponse
import json


# Create your views here.
def landing(request):
    d = {}
    return render(request, 'landing_page.html', d)


def home(request):
    d = {}
    return render(request, 'home.html', d)

def new_mail(request):
    print "AAA"
    '''if request.method == 'POST' and request.FILES['my_file']:'''
    if request.method == 'POST':
        mail_type = request.POST.get('mail_type')
        sender = request.POST.get('sender')
        print ">>>"
        print mail_type
        print sender

    d = {}
    d["pagetitle"] = "New mails"
    d["mail_types"] = MailType.objects.all()
    d["senders"] = Sender.objects.all()

    return render(request, 'new_mail.html', d)


def save_mail(request):
    print "BBB"
    response_data = {}
    if request.method == 'POST':
        #import pdb; pdb.set_trace()
        json_data = json.loads(request.body)
        mail_type = json_data['mail_type']
        sender = json_data['sender']
        
        mail_type_object = MailType.objects.filter(id=mail_type)
        sender_object = Sender.objects.filter(id=sender)

        if len(mail_type_object) > 0:
            mail_type_object = mail_type_object[0]
            print mail_type_object
        if len(sender_object) > 0:
            sender_object = sender_object[0]
            print sender_object

        Mail.objects.create(sender = sender_object, mail_type = mail_type_object)

        return HttpResponse(response_data, content_type="application/json")


def track_mail(request):
    d = {}
    return render(request, 'track_mail.html', d)
