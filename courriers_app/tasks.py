from courriers_app.models import *
import datetime
from django.shortcuts import render
from django.db.models import F, Q
import unicodedata
from django.core.mail import send_mail
from django.db.models import Max
from threading import Thread
from django.views.decorators.csrf import csrf_exempt
from jsonview.decorators import json_view


@csrf_exempt
@json_view
def alert_for_pending_invoices_1(request):
	"""This function receives requests sent by RapidPro. 
	This function send json data to RapidPro as a response."""

	print(">>>>>>>>>>>>>>>>>>>>>Beginning of alert_for_pending_invoices_1<<<<<<<<<<<<<<<<<<<<")

	Thread(target=alert_for_pending_invoices_1_woker).start()

	print(">>>>>>>>>>>>>>>>>>>>>End of alert_for_pending_invoices_1<<<<<<<<<<<<<<<<<<<<")

	response = {}

	response["info_to_contact"] = "Ok"

	return response


def alert_for_pending_invoices_1_woker():
	''' This function informs a staff that there is/are (an) invoice(s) pending on his/her desk '''
	invoice_accepted_proc_days_set = Settings.objects.filter(setting_name = "INVOICE_ACCEPTED_PROC_DAYS_1")
	if len(invoice_accepted_proc_days_set) < 1:
		print("Please, create INVOICE_ACCEPTED_PROC_DAYS_1 in Settings model")
		return

	invoice_accepted_proc_days_record = invoice_accepted_proc_days_set[0]

	invoice_accepted_proc_days = int(invoice_accepted_proc_days_record.setting_value)

	minimum_registration_date = datetime.datetime.now().date() - datetime.timedelta(days=invoice_accepted_proc_days)

	all_concerned_invoinces = (
		Track.objects.filter(mail__closed = False)
		.annotate(max_date = Max("mail__track__start_date"))
		.filter(start_date = F('max_date'),
			end_date__isnull = True,
			mail__mail_type__mail_type_name__iexact = "invoice",
			mail__recorded_time__lte = minimum_registration_date)
		.annotate(staff_f_name = F('staff__first_name'))
		.annotate(email = F('staff__user__email'))
		.annotate(mail_number = F('mail__number'))
		).values()

	concerned_staffs = {}

	for one_invoice in all_concerned_invoinces:
		one_concerned_staff = {}
		one_concerned_staff["staff_email"] = one_invoice["email"]
		one_concerned_staff["staff_first_name"] = one_invoice["staff_f_name"]
		mail_number = unicodedata.normalize('NFKD', one_invoice["mail_number"]).encode('ascii', 'ignore')
		one_concerned_staff["mail_numbers"] = [mail_number]

		if one_concerned_staff["staff_email"] in concerned_staffs:
			concerned_staffs[one_concerned_staff["staff_email"]]["mail_numbers"].append(mail_number)
		else:
			concerned_staffs[one_concerned_staff["staff_email"]] = one_concerned_staff

	if len(concerned_staffs) > 0:
		#We have staffs to notify
		for one_email in concerned_staffs:
			print("")
			print("")
			print(">>>>>>")
			if(len(concerned_staffs[one_email]["mail_numbers"]) > 1):
				e_mail_body = ("Dear "+concerned_staffs[one_email]["staff_first_name"]+", "+
					"This is to let you know that on your desk you have "+
					"invoices that last several days in the system."+
					" The numbers of those invoices are "+str(concerned_staffs[one_email]["mail_numbers"])+"."+
					" Best regards.")
			else:
				e_mail_body = ("Dear "+concerned_staffs[one_email]["staff_first_name"]+", "+
					"This is to let you know that on your desk you have "+
					"an invoice that last several days in the system."+
					" The number of that invoice is "+str(concerned_staffs[one_email]["mail_numbers"])+"."+
					" Best regards.")

			#e_mail_body = "Dear "+concerned_staffs[one_email]["staff_first_name"]+", This is to let you know that on your desk you have invoices that last several days in the system. Best regards."

			e_mail_subject = "Push and Track - Alert on voices last serval days under processing"

			e_mail_sender = "noreply@pushandtrack.org"

			e_mail_receiver = concerned_staffs[one_email]["staff_email"]


			#Before sending an email, let's check if this staff is not deleted
			the_concerned_staff_set = Staff.objects.filter(user__email = one_email)
			if(len(the_concerned_staff_set) > 0):
				the_concerned_staff = the_concerned_staff_set[0]
				if not the_concerned_staff.is_deleted:
					print(e_mail_body)
					send_mail(e_mail_subject, e_mail_body, e_mail_sender, [e_mail_receiver,])











@csrf_exempt
@json_view
def alert_for_pending_mails_1(request):
	"""This function receives requests sent by RapidPro. 
	This function send json data to RapidPro as a response."""

	print(">>>>>>>>>>>>>>>>>>>>>Beginning of alert_for_pending_mails_1<<<<<<<<<<<<<<<<<<<<")

	Thread(target=alert_for_pending_mails_1_worker).start()

	print(">>>>>>>>>>>>>>>>>>>>>End of alert_for_pending_mails_1<<<<<<<<<<<<<<<<<<<<")

	response = {}

	response["info_to_contact"] = "Ok"

	return response



def alert_for_pending_mails_1_worker():
	''' This function informs a staff that there is/are (a) mail(s) pending on his/her desk '''
	mail_accepted_proc_days_set = Settings.objects.filter(setting_name = "MAIL_ACCEPTED_PROC_DAYS_1")
	if len(mail_accepted_proc_days_set) < 1:
		print("Please, create MAIL_ACCEPTED_PROC_DAYS_1 in Settings model")
		return

	mail_accepted_proc_days_record = mail_accepted_proc_days_set[0]

	mail_accepted_proc_days = int(mail_accepted_proc_days_record.setting_value)

	minimum_registration_date = datetime.datetime.now().date() - datetime.timedelta(days=mail_accepted_proc_days)

	all_concerned_mails = (
		Track.objects.filter(mail__closed = False)
		.annotate(max_date = Max("mail__track__start_date"))
		.filter(start_date = F('max_date'),
			end_date__isnull = True,
			mail__mail_type__mail_type_name__iexact = "mail",
			mail__recorded_time__lte = minimum_registration_date)
		.annotate(staff_f_name = F('staff__first_name'))
		.annotate(email = F('staff__user__email'))
		.annotate(mail_number = F('mail__number'))
		).values()

	concerned_staffs = {}

	for one_mail in all_concerned_mails:
		one_concerned_staff = {}
		one_concerned_staff["staff_email"] = one_mail["email"]
		one_concerned_staff["staff_first_name"] = one_mail["staff_f_name"]
		mail_number = unicodedata.normalize('NFKD', one_mail["mail_number"]).encode('ascii', 'ignore')
		one_concerned_staff["mail_numbers"] = [mail_number]

		if one_concerned_staff["staff_email"] in concerned_staffs:
			concerned_staffs[one_concerned_staff["staff_email"]]["mail_numbers"].append(mail_number)
		else:
			concerned_staffs[one_concerned_staff["staff_email"]] = one_concerned_staff

	if len(concerned_staffs) > 0:
		#We have staffs to notify. Let's notify them
		for one_email in concerned_staffs:
			print("")
			print("")
			print(">>>>>>")
			if(len(concerned_staffs[one_email]["mail_numbers"]) > 1):
				e_mail_body = ("Dear "+concerned_staffs[one_email]["staff_first_name"]+", "+
					"This is to let you know that on your desk you have "+
					"mails that last several days in the system."+
					" The numbers of those mails are "+str(concerned_staffs[one_email]["mail_numbers"])+"."+
					" Best regards.")
			else:
				e_mail_body = ("Dear "+concerned_staffs[one_email]["staff_first_name"]+", "+
					"This is to let you know that on your desk you have "+
					"a mail that last several days in the system."+
					" The number of that mail is "+str(concerned_staffs[one_email]["mail_numbers"])+"."+
					" Best regards.")

			#e_mail_body = "Dear "+concerned_staffs[one_email]["staff_first_name"]+", This is to let you know that on your desk you have invoices that last several days in the system. Best regards."

			e_mail_subject = "Push and Track - Alert on voices last serval days under processing"

			e_mail_sender = "noreply@pushandtrack.org"

			e_mail_receiver = concerned_staffs[one_email]["staff_email"]


			#Before sending an email, let's check if this staff is not deleted
			the_concerned_staff_set = Staff.objects.filter(user__email = one_email)
			if(len(the_concerned_staff_set) > 0):
				the_concerned_staff = the_concerned_staff_set[0]
				if not the_concerned_staff.is_deleted:
					print(e_mail_body)
					send_mail(e_mail_subject, e_mail_body, e_mail_sender, [e_mail_receiver,])










@csrf_exempt
@json_view
def alert_for_pending_dct_1(request):
	"""This function receives requests sent by RapidPro. 
	This function send json data to RapidPro as a response."""

	print(">>>>>>>>>>>>>>>>>>>>>Beginning of alert_for_pending_dct_1<<<<<<<<<<<<<<<<<<<<")

	Thread(target=alert_for_pending_dct_1_worker).start()

	print(">>>>>>>>>>>>>>>>>>>>>End of alert_for_pending_dct_1<<<<<<<<<<<<<<<<<<<<")

	response = {}

	response["info_to_contact"] = "Ok"

	return response



def alert_for_pending_dct_1_worker():
	''' This function informs a staff that there is/are (a) mail(s) pending on his/her desk '''
	mail_accepted_proc_days_set = Settings.objects.filter(setting_name = "MAIL_ACCEPTED_PROC_DAYS_1")
	if len(mail_accepted_proc_days_set) < 1:
		print("Please, create MAIL_ACCEPTED_PROC_DAYS_1 in Settings model")
		return

	mail_accepted_proc_days_record = mail_accepted_proc_days_set[0]

	mail_accepted_proc_days = int(mail_accepted_proc_days_record.setting_value)

	minimum_registration_date = datetime.datetime.now().date() - datetime.timedelta(days=mail_accepted_proc_days)

	all_concerned_mails = (
		Track.objects.filter(mail__closed = False)
		.annotate(max_date = Max("mail__track__start_date"))
		.filter(start_date = F('max_date'),
			end_date__isnull = True,
			mail__mail_type__mail_type_name__iexact = "DCT",
			mail__recorded_time__lte = minimum_registration_date)
		.annotate(staff_f_name = F('staff__first_name'))
		.annotate(email = F('staff__user__email'))
		.annotate(mail_number = F('mail__number'))
		).values()

	concerned_staffs = {}

	for one_mail in all_concerned_mails:
		one_concerned_staff = {}
		one_concerned_staff["staff_email"] = one_mail["email"]
		one_concerned_staff["staff_first_name"] = one_mail["staff_f_name"]
		mail_number = unicodedata.normalize('NFKD', one_mail["mail_number"]).encode('ascii', 'ignore')
		one_concerned_staff["mail_numbers"] = [mail_number]

		if one_concerned_staff["staff_email"] in concerned_staffs:
			concerned_staffs[one_concerned_staff["staff_email"]]["mail_numbers"].append(mail_number)
		else:
			concerned_staffs[one_concerned_staff["staff_email"]] = one_concerned_staff

	if len(concerned_staffs) > 0:
		#We have staffs to notify. Let's notify them
		for one_email in concerned_staffs:
			print("")
			print("")
			print(">>>>>>")
			if(len(concerned_staffs[one_email]["mail_numbers"]) > 1):
				e_mail_body = ("Dear "+concerned_staffs[one_email]["staff_first_name"]+", "+
					"This is to let you know that on your desk you have "+
					"mails that last several days in the system."+
					" The numbers of those mails are "+str(concerned_staffs[one_email]["mail_numbers"])+"."+
					" Best regards.")
			else:
				e_mail_body = ("Dear "+concerned_staffs[one_email]["staff_first_name"]+", "+
					"This is to let you know that on your desk you have "+
					"a mail that last several days in the system."+
					" The number of that mail is "+str(concerned_staffs[one_email]["mail_numbers"])+"."+
					" Best regards.")

			#e_mail_body = "Dear "+concerned_staffs[one_email]["staff_first_name"]+", This is to let you know that on your desk you have invoices that last several days in the system. Best regards."

			e_mail_subject = "Push and Track - Alert on voices last serval days under processing"

			e_mail_sender = "noreply@pushandtrack.org"

			e_mail_receiver = concerned_staffs[one_email]["staff_email"]


			#Before sending an email, let's check if this staff is not deleted
			the_concerned_staff_set = Staff.objects.filter(user__email = one_email)
			if(len(the_concerned_staff_set) > 0):
				the_concerned_staff = the_concerned_staff_set[0]
				if not the_concerned_staff.is_deleted:
					print(e_mail_body)
					send_mail(e_mail_subject, e_mail_body, e_mail_sender, [e_mail_receiver,])