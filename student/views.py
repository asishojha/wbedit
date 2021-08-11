from django.shortcuts import render, redirect
from django.contrib import messages
from django.forms.models import model_to_dict
from datetime import datetime
from .models import Student
from .forms import StudentForm

def student(request, serial):
	student = Student.objects.filter(school=request.user, serial=serial)[0]
	context = {
		'student': student
	}
	return render(request, 'student/student.html', context)

def select_student(request, serial):
	student = Student.objects.filter(school=request.user, serial=serial)[0]
	student.selected = True
	student.save()

	try:
		next_student = Student.objects.filter(school=request.user, serial__gt=serial).first()
		messages.success(request, f'Student {student.name} has been marked as Selected')
		return redirect(next_student.get_absolute_url())
	except Exception:
		next_student = None
		return redirect('school:student_list')


def not_select_student(request, serial):
	student = Student.objects.filter(school=request.user, serial=serial)[0]
	student.not_selected = True
	student.save()

	try:
		next_student = Student.objects.filter(school=request.user, serial__gt=serial).first()
		messages.warning(request, f'Student {student.name} has been marked as NOT Selected')
		return redirect(next_student.get_absolute_url())
	except Exception:
		next_student = None
		return redirect('school:student_list')

def edit_student(request, serial):
	student = Student.objects.filter(school=request.user, serial=serial)[0]
	student_dict = model_to_dict(student, fields=[field.name for field in student._meta.fields])
	student_dict['g_name'] = student.get_guardian_name()
	student_dict['dob'] = datetime.strptime(student_dict['dob'], '%d%m%y')
	form = StudentForm(initial=student_dict)

	if request.method == 'POST':
		form = StudentForm(request.POST)
		if form.is_valid():
			dob = form.cleaned_data.get('dob')
			s = form.save(commit=False)
			s.dob = dob.strftime('%d%m%y')
			s.save()
			messages.success(request, f"Information for student {student.name} has been updated. Please SELECT / NOT SELECT the student.")
			return redirect(student.get_absolute_url())

	context = {
		'form': form
	}
	return render(request, 'student/form.html', context)