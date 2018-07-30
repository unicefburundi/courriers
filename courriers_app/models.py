# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Sender(models.Model):
    '''In this model, we will store providers'''
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=100,blank=True)
    phone_number = models.CharField(max_length=50)

    def __unicode__(self):
        return "{0} - Tel : {1}".format(self.first_name, self.phone_number)


class StaffPosition(models.Model):
    '''In this model, we will store staff functions'''
    designation = models.CharField(max_length=50)

    def __unicode__(self):
        return "{0}".format(self.designation)

class Section(models.Model):
    '''In this model, we will store sections'''
    designation = models.CharField(max_length=50)

    def __unicode__(self):
        return "{0}".format(self.designation)

class Staff(models.Model):
    '''In this model, we will store sections'''
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    section = models.ForeignKey(Section)
    function = models.ForeignKey(StaffPosition)
    email = models.EmailField(max_length=100)
    office_phone_number = models.CharField(max_length=20)
    mobile_phone_number = models.CharField(max_length=20)

    def __unicode__(self):
        return "{0} {1}".format(self.first_name, self.last_name)

class MailType(models.Model):
    '''In this model, we will store mail types'''
    mail_type_name = models.CharField(max_length=50)

    def __unicode__(self):
        return "{0}".format(self.mail_type_name)

class Mail(models.Model):
    '''In this model, we will store mails and invoices'''
    number = models.CharField(max_length=20, unique=True)
    sender = models.ForeignKey(Sender)
    mail = models.ImageField(null=True)
    mail_type = models.ForeignKey(MailType)
    received_time = models.DateTimeField(auto_now_add=True, blank=True)

    def __unicode__(self):
        return "{0} - Mail type : {1} - Registered {2}".format(self.sender.first_name, self.mail_type.mail_type_name, self.received_time)

class track(models.Model):
    '''In this model, we will record wherever a mail went through'''
    mail = models.ForeignKey(Mail)
    staff = models.ForeignKey(Staff)
    start_date = models.DateTimeField(auto_now_add=True, blank=True)
    purpose = models.CharField(max_length=100)
    end_date = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        return "{0} [Registered {1}] - {2} - Start {3} - End {4}".format(self.mail.sender.first_name, self.mail.received_time, self.staff.first_name, self.start_date, self.end_date)
