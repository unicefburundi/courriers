# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Sender(models.Model):
    '''In this model, we will store providers'''
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, null=True)
    email = models.EmailField(max_length=100,blank=True, null=True)
    phone_number = models.CharField(max_length=50, null=True)

    def __unicode__(self):
        return "{0} - Tel : {1} - Sender ID : {2}".format(self.first_name, self.phone_number, self.id)


class StaffPosition(models.Model):
    '''In this model, we will store staff functions'''
    designation = models.CharField(max_length=50)

    def __unicode__(self):
        return "{0} - Staff Position ID : {1}".format(self.designation, self.id)

class Section(models.Model):
    '''In this model, we will store sections'''
    designation = models.CharField(max_length=50)

    def __unicode__(self):
        return "{0} - Section ID : {1}".format(self.designation, self.id)

class Staff(models.Model):
    '''In this model, we will store Staff details'''
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    section = models.ForeignKey(Section, null=True)
    function = models.ForeignKey(StaffPosition, null=True)
    #email = models.EmailField(max_length=100)
    office_phone_number = models.CharField(max_length=20, null=True)
    mobile_phone_number = models.CharField(max_length=20, null=True)
    is_deleted = models.BooleanField(default=False)

    def __unicode__(self):
        return "{0} {1} - {2} - Staff id {3} - is deleted? {4}".format(self.first_name, self.last_name, self.user.email, self.id, self.is_deleted)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Staff.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    print("A")
    instance.staff.save()
    print("B")

class MailType(models.Model):
    '''In this model, we will store mail types'''
    mail_type_name = models.CharField(max_length=50)

    def __unicode__(self):
        return "{0} - Mail type id {1}".format(self.mail_type_name, self.id)

class Mail(models.Model):
    '''In this model, we will store mails and invoices'''
    external_number = models.CharField(max_length=100, null=True)
    number = models.CharField(max_length=100, unique=True)
    sender = models.ForeignKey(Sender)
    mail = models.ImageField(null=True)
    mail_type = models.ForeignKey(MailType)
    received_time = models.DateTimeField(blank=True)
    recorded_time = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    closed = models.BooleanField(default=False)
    closed_time = models.DateTimeField(null=True)
    need_answer = models.BooleanField(default=False)
    answered = models.BooleanField(default=False)
    soft_copy = models.FileField(upload_to ='uploads/', null=True)
    closure_reason = models.CharField(max_length=300, null=True)
    closed_by = models.ForeignKey(Staff, null=True)

    def __unicode__(self):
        return "{0} - Mail type : {1} - Registered {2} - Isclosed {3} - Mail id {4} - Sender id {5} - Mail Type id {6}".format(self.sender.first_name, self.mail_type.mail_type_name, self.received_time, self.closed, self.id, self.sender.id, self.mail_type.id)

class Track(models.Model):
    '''In this model, we will record wherever a mail went through'''
    mail = models.ForeignKey(Mail)
    staff = models.ForeignKey(Staff)
    start_date = models.DateTimeField(auto_now_add=True, blank=True)
    hard_copy_transfer_time = models.DateTimeField(null=True)
    purpose = models.CharField(max_length=300)
    end_date = models.DateTimeField(blank=True, null=True)
    soft_copy = models.FileField(upload_to ='uploads/', null=True)

    def __unicode__(self):
        return "{0} [Registered {1}] - {2} - Start {3} - End {4} - Mail id {5} - Staff id {6}".format(self.mail.sender.first_name, self.mail.received_time, self.staff.first_name, self.start_date, self.end_date, self.mail.id, self.staff.id)



class TimeMeasuringUnit(models.Model):
    """
    This model is used to store time measuring units
    """

    code = models.CharField(max_length=4)
    description = models.CharField(max_length=20)

    def __unicode__(self):
        return "{0} - {1}".format(self.code, self.description)


class Settings(models.Model):
    """
    In this model we will put settings
    """

    setting_name = models.CharField(max_length=200)
    setting_value = models.CharField(max_length=100)
    time_measuring_unit = models.ForeignKey(TimeMeasuringUnit, null=True)
    # Change the above line. It should accept null. It doesn't accept null values for the moment

    def __unicode__(self):
        return "{0} - {1} - {2}".format(self.setting_name, self.setting_value, self.time_measuring_unit)