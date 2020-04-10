# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from courriers_app.models import Staff


class Binome(models.Model):
    '''In this model, we will store Binomes'''
    staff_1 = models.ForeignKey(Staff, related_name='the_selecter')
    staff_2 = models.ForeignKey(Staff, related_name='the_selected')

    def __unicode__(self):
        return "{0} - {1}".format(self.staff_1, self.staff_2)

class NotAvailable(models.Model):
    '''In this model, we will store not available staffs'''
    staff = models.OneToOneField(Staff, on_delete=models.CASCADE)

    def __unicode__(self):
        return "{0}".format(self.staff)
