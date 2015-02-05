from django.conf import settings

from django.shortcuts import render, HttpResponseRedirect, Http404

from .models import Join
from .forms import JoinForm
# from .forms import EmailForm

from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives

def get_ip(request):
	x_forward = request.META.get("HTTP_X_FORWARDED_FOR")
	try:
		if x_forward:
			ip = x_forward.split(",")[0]
		else:
			ip = request.META.get("REMOTE_ADDR")
	except:
		ip = ""

	return ip

# module for helping us generate a unique id for user
import uuid

def create_id():
	ref_id = str(uuid.uuid4())[:11].replace('-', '').lower()
	try:
		exists = Join.objects.get(ref_id = ref_id)
		create_id()
	except:
		return ref_id

def legal(request):
	try:
		context = {}
		template = "legal.html"
		return render(request, template, context)
	except:
		raise Http404

def logodesign(request):
	try:
		context = {}
		template = "logodesign.html"
		return render(request, template, context)
	except:
		raise Http404

def share(request, ref_id):
	# For debugging purposes
	# print ref_id
	
	try:
		join_obj = Join.objects.get(ref_id = ref_id)
		obj = Join.objects.filter(friend = join_obj)
		count = join_obj.referral.count()
		ref_url = settings.SHARE_URL + str(join_obj.ref_id) 
		context = {"ref_id": join_obj.ref_id, "count": count, "ref_url": ref_url}
		template = "share.html"
		return render(request, template, context)
	except:
		raise Http404


def home(request):
	try:
		brought_by_id = request.session['brought_by_id']
		obj = Join.objects.get(id = brought_by_id)
	except:
		obj = None

	#Command for viewing the request in terminal for debugging purpose
	#print request
	
	# form = EmailForm(request.POST or None)
	# if form.is_valid():
	# email = form.cleaned_data['email']
	# new_join, created = Join.objects.get_or_create(email = email)
	# 	print new_join, created
	# 	if created:
	# 		print new_join.timestamp

	form = JoinForm(request.POST or None)

	if form.is_valid():
		new_join = form.save(commit = False)
		email = form.cleaned_data['email']
		new_join_old, created = Join.objects.get_or_create(email = email)
		if created:
			if not obj == None:
				new_join_old.friend = obj
			new_join_old.ref_id = create_id()
			new_join_old.ip_address = get_ip(request)
			new_join_old.save()

			## Email using EmailMessage (plaintext)
			# email = EmailMessage('Subject', 'Body', to=["akashtndn.acm@gmail.com"])
			# email.send()

			## Email using EmailMultiAlternatives (text/html)
			subject, from_email, to = 'Welcome to Skifer', 'Skifer.India@gmail.com', "akashtndn.acm@gmail.com"
			text_content = 'Thanks for dropping by and registering. We are currently in a building phase, and are trying our best to make Skifer an awesome experience for you. We will make sure that you are the first to know when we launch. Again, we appreciate your show of faith in us. Regards, Team Skifer'
			html_content = '<p>Thanks for dropping by and registering. We are currently in a building phase, and are trying our best to make Skifer an awesome experience for you. <br> We will make sure that you are the first to know when we launch. <br> </p> <p>Again, we appreciate your show of faith in us. <br><br> Regards, <br><strong>Team Skifer</strong></p>'
			msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
			msg.attach_alternative(html_content, "text/html")
			msg.send()

		# new_join.ip_address = get_ip(request)
		# new_join.save()
		return HttpResponseRedirect("/%s" %(new_join_old.ref_id))


	context = {'form': form}
	template = "flatty_landing.html"
	return render(request, template, context)