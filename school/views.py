from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Permission
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.template.loader import get_template
from django.contrib.contenttypes.models import ContentType
from .models import Profile
from .forms import UsersLoginForm, ProfileForm, PasswordResetForm
from student.models import Student

import pdfkit
import time
# from .downloads import download_pdf

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
		
		ct = ContentType.objects.get_for_model(User)
		permission_change_password, created_change_password = Permission.objects.get_or_create(codename='can_change_password', name='Can change the password', content_type=ct)


		try:
			user.profile
			if not user.has_perm('auth.can_change_password'):
				return redirect('school:student_list')
			return redirect('school:reset_password')
		except Profile.DoesNotExist:
			return redirect("school:profile")
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
	try:
		request.user.profile
		pass
	except Profile.DoesNotExist:
		return redirect('school:profile')

	if not request.user.has_perm('auth.can_change_password'):
		pass
	else:
		return redirect('school:reset_password')
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

@login_required
def submit_final_data(request):
	school = request.user
	profile = school.profile
	pending_students = school.student_set.filter(status=None)
	
	if pending_students.count():
		messages.warning(request, 'Please make sure that all the students are marked as either SELECTED or NOT SELECTED')
		return redirect('school:student_list')

	if profile.complete:
		messages.success(request, 'Final Data is already submitted for your students. Please download the report.')
		return redirect('school:student_list')		

	if request.method == 'POST':
		agree = request.POST.get('agree')
		verification_name = request.POST.get('verification_name')

		if agree:
			profile.complete = True
			profile.verification_name = verification_name
			profile.save()
			messages.success(request, 'Congratulations! All your data has been finally submitted. Your can now download the report generated.')
			return redirect('school:student_list')
	return render(request, 'school/submit-data.html')

@login_required
def pdf_report(request):
	template = get_template('school/pdf-report.html')
	output = template.render(context={'school': request.user})
	time.sleep(2)
	options = {
        'page-size': 'A4',
        'margin-top': '0.5in',
        'margin-right': '0.5in',
        'margin-bottom': '0.5in',
        'margin-left': '0.5in',
        'encoding': "UTF-8",
        'orientation': 'landscape'
    }
	pdf = pdfkit.from_string(output, False, options)
	response = HttpResponse(pdf, content_type='application/pdf')
	response['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(request.user.username)
	return response

@login_required
def profile(request):
	user = request.user
	try:
		request.user.profile
		return redirect('school:student_list')
	except Profile.DoesNotExist:
		pass
	form = ProfileForm()
	if request.method == 'POST':
		form = ProfileForm(request.POST)
		if form.is_valid():
			profile = form.save(commit=False)
			profile.school = user
			profile.save()
			user.email = profile.headmaster_email
			user.save()
			permission = Permission.objects.get(codename='can_change_password')
			user.user_permissions.add(permission)
			return redirect('school:reset_password')
	context = {
		'form': form
	}
	return render(request, 'school/profile.html', context)

@login_required
def reset_password(request):
	if not request.user.has_perm('auth.can_change_password'):
		try:
			request.user.profile
			return redirect('school:student_list')
		except Profile.DoesNotExist:
			return redirect('school:profile')

	form = PasswordResetForm(request.user)
	password_change_permission = Permission.objects.get(codename='can_change_password')
	if request.method == 'POST':
		form = PasswordResetForm(request.user, request.POST)
		if form.is_valid():
			password = form.save()
			update_session_auth_hash(request, password)
			request.user.user_permissions.remove(password_change_permission)

			request.user.profile.password_changed = True
			request.user.profile.save()

			messages.success(request, 'Password Changed Successfully!')
			return redirect('school:student_list')
	context = {
		'form': form
	}
	return render(request, 'accounts/reset-password.html', context)

def instructions(request):
	return render(request, 'school/instructions.html')

@user_passes_test(lambda u:u.is_staff, login_url='/admin/login/')
def school_status(request):
	profile_created_schools = Profile.objects.all().count()
	selected_students = Student.objects.filter(status='1').count()
	not_selected_students = Student.objects.filter(status='2').count()
	edited_students = Student.objects.filter(edited=True).count()
	completed_profiles = Profile.objects.filter(complete=True).count()

	context = {
		'profile_created_schools': profile_created_schools,
		'selected_students': selected_students,
		'not_selected_students': not_selected_students,
		'edited_students': edited_students,
		'completed_profiles': completed_profiles
	}
	return render(request, 'school/live_data_status.html', context)

def download_pdfs():
	schools = User.objects.exclude(is_staff=True)
	for school in schools:
		# download_pdf(school)
		print('Downloading PDF for school', school.username)
