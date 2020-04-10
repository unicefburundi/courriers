# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from courriers_app.models import Staff
from django.db.models import F

def binome(request):
    d = {}

    the_connected_user = request.user

    try:
    	the_connected_staff = the_connected_user.staff
    except:
    	message_to_user = "Your are not well recorded in the system. Please contact the system admin. Thank you"
    	d["staff"] = (Staff.objects.all()
    		.exclude(user = the_connected_user)
    		.exclude(notavailable__isnull=True)
    		.annotate(section_name = F('section__designation'))
    		.order_by("first_name"))
    	return render(request, 'binomes.html', d)


    if request.method == 'POST':
    	chosen_staff = request.POST.get('staff')

    	#We put thise persons in the list of unavailable staff
    	try:
    		NotAvailable.objects.create(staff = the_connected_staff)
    	except:
    		message_to_user = "Sorry. Someone has just choose you. Thank you"
	    	d["staff"] = (Staff.objects.all()
	    		.exclude(user = the_connected_user)
	    		.exclude(notavailable__isnull=True)
	    		.annotate(section_name = F('section__designation'))
	    		.order_by("first_name"))
	    	return render(request, 'binomes.html', d)

        try:
            NotAvailable.objects.create(staff = chosen_staff)
        except:
            message_to_user = "Sorry. Someone has just choose the staff you pick. Please choose another one. Thank you"
            NotAvailable.objects.filter(staff = the_connected_staff).delete()
            d["staff"] = (Staff.objects.all()
                .exclude(user = the_connected_user)
                .exclude(notavailable__isnull=True)
                .annotate(section_name = F('section__designation'))
                .order_by("first_name"))
            return render(request, 'binomes.html', d)

    	#We create a binome
    	created_binome = Binome.objects.create(
    		staff_1 = the_connected_staff,
    		staff_2 = chosen_staff)

        d["staff"] = (Staff.objects.all()
            .exclude(user = the_connected_user)
            .exclude(notavailable__isnull=False)
            .annotate(section_name = F('section__designation'))
            .order_by("first_name"))
        return render(request, 'binomes.html', d)


    d["staff"] = (Staff.objects.all()
    	.exclude(user = the_connected_user)
    	.exclude(notavailable__isnull=False)
    	.annotate(section_name = F('section__designation'))
    	.order_by("first_name"))
    return render(request, 'binomes.html', d)
