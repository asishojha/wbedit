from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Profile
from .forms import UsersLoginForm
from student.models import Student

import weasyprint

def index(request):
	return render(request, 'school/index.html')

def login_view(request):
	if request.user.is_authenticated:
		return redirect('school:index')
	form = UsersLoginForm(request.POST or None)
	if form.is_valid():
		username = form.cleaned_data.get("username")
		password = form.cleaned_data.get("password")
		user = authenticate(username = username, password = password)
		login(request, user)
		return redirect('school:student_list')
		# if user.has_perm('marks.can_update'):
			# return redirect('marks:students')
		# else:
		# try:
			# profile = request.user.profile
			# if not user.has_perm('marks.can_change_password'):
				# return redirect('marks:students')
			# else:
				# return redirect('marks:reset_password')
		# except Profile.DoesNotExist:
			# return redirect("school:profile")
	return render(request, "accounts/form.html", {
		"form" : form,
		"title" : "Login",
	})

@login_required
def logout_view(request):
	logout(request)
	return redirect("/")

@login_required
def student_list(request):
	male_students = Student.objects.filter(school=request.user, sex='1')
	female_students = Student.objects.filter(school=request.user, sex='2')
	total_students = Student.objects.filter(school=request.user)
	selected_students = Student.objects.filter(school=request.user, status='1')
	not_selected_students = Student.objects.filter(school=request.user, status='2')
	pending_students = Student.objects.filter(school=request.user, status=None)

	paginator = Paginator(total_students, 15)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)

	try:
		first_student = pending_students[0]
	except IndexError:
		first_student = None
	
	context = {
		'userx': request.user,
		'male_students': male_students.count(),
		'female_students': female_students.count(),
		'total_students': total_students.count(),
		'selected_students': selected_students.count(),
		'not_selected_students': not_selected_students.count(),
		'pending_students': pending_students.count(),
		'page_obj': page_obj,
		'first_student': first_student

	}
	return render(request, 'school/student_list.html', context)

def submit_final_data(request):
	if request.method == 'POST':
		agree = request.POST.get('agree')
		if agree:
			profile = request.user.profile
			profile.complete = True
			profile.save()
			messages.success(request, 'Congratulations! All your data has been finally submitted. Your can now download the report generated.')
			return redirect('school:student_list')
	return render(request, 'school/submit-data.html')

def pdf_report(request):
	html = render_to_string('school/pdf-report.html', {'school': request.user})
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'filename=\
	"{}.pdf"'.format(request.user.username)
	weasyprint.HTML(string=html, base_url=request.build_absolute_uri()).write_pdf(response)
	return response