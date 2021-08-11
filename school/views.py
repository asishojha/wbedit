from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Profile
from .forms import UsersLoginForm
from student.models import Student

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
	selected_students = Student.objects.filter(school=request.user, selected=True)
	not_selected_students = Student.objects.filter(school=request.user, not_selected=True)

	paginator = Paginator(total_students, 15)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	
	context = {
		'userx': request.user,
		'male_students': male_students.count(),
		'female_students': female_students.count(),
		'total_students': total_students.count(),
		'selected_students': selected_students.count(),
		'not_selected_students': not_selected_students.count(),
		'page_obj': page_obj

	}
	return render(request, 'school/student_list.html', context)