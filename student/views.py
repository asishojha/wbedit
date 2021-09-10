from django.shortcuts import render, redirect
from django.contrib import messages
from django.forms.models import model_to_dict
from datetime import datetime
from .models import Student, SupportDocument
from .forms import StudentForm
from .decorators import can_edit_data

@can_edit_data
def student(request, serial):
	student = Student.objects.filter(school=request.user, serial=serial)[0]
	context = {
		'student': student
	}
	return render(request, 'student/student.html', context)

@can_edit_data
def select_student(request, serial):
	student = Student.objects.filter(school=request.user, serial=serial)[0]
	student.status = '1'
	student.save()

	try:
		next_student = Student.objects.filter(school=request.user, serial__gt=serial).first()
		messages.success(request, f'Student {student.name} has been marked as Selected')
		return redirect(next_student.get_absolute_url())
	except Exception:
		return redirect('school:student_list')

@can_edit_data
def not_select_student(request, serial):
	student = Student.objects.filter(school=request.user, serial=serial)[0]
	student.status = '2'
	student.save()

	try:
		next_student = Student.objects.filter(school=request.user, serial__gt=serial).first()
		messages.warning(request, f'Student {student.name} has been marked as NOT Selected')
		return redirect(next_student.get_absolute_url())
	except Exception:
		return redirect('school:student_list')

@can_edit_data
def edit_student(request, serial):
	student = Student.objects.filter(school=request.user, serial=serial)[0]
	student_dict = model_to_dict(student, fields=[field.name for field in student._meta.fields])
	student_dict['g_name'] = student.get_guardian_name()
	student_dict['dob'] = datetime.strptime(student_dict['dob'], '%d%m%y')

	try:
		document = SupportDocument.objects.get(student=student).document
	except SupportDocument.DoesNotExist:
		document = None

	student_dict['document'] = document

	form = StudentForm(initial=student_dict)

	if request.method == 'POST':
		form = StudentForm(request.POST, instance=student)
		if form.is_valid():
			support_document = form.cleaned_data.get('document')
			edited = form.cleaned_data.get('edited')
			form.cleaned_data.pop('edited')
			s = form.save(commit=False)
			dob = form.cleaned_data.get('dob').strftime('%d%m%y')
			s.dob = dob
			if edited == '1':
				s.edited = True

				s_document, s_document_created = SupportDocument.objects.get_or_create(student=student)
				s_document.document = support_document
				s_document.save()
			s.save()
			messages.success(request, f"Information for student {student.name} has been updated. Please SELECT / NOT SELECT the student.")
			return redirect(student.get_absolute_url())

	context = {
		'form': form
	}
	return render(request, 'student/form.html', context)

# def support_document(request, serial):
# 	student = Student.objects.filter(school=request.user, serial=serial)[0]
# 	try:
# 		support_document = SupportDocument.objects.get(student=student)
# 	except SupportDocument.DoesNotExist:
# 		support_document = None
# 	form = SupportDocumentForm(instance=support_document)
# 	if request.method == 'POST':
# 		form = SupportDocumentForm(request.POST, instance=support_document)
# 		if form.is_valid():
# 			document = form.save(commit=False)
# 			document.student = student
# 			document.save()
# 			messages.success(request, f"Information for student {student.name} has been updated. Please SELECT / NOT SELECT the student.")
# 			return redirect(student.get_absolute_url())
# 	context = {
# 		'form': form
# 	}
# 	return render(request, 'student/form.html', context)
