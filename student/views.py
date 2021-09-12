from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from datetime import datetime
from .models import Student, SupportDocument
from .forms import StudentForm
from .decorators import can_edit_data
from school.models import Profile

@login_required
@can_edit_data
def student(request, serial):
	try:
		profile = request.user.profile
		pass
	except Profile.DoesNotExist:
		return redirect('school:profile')

	student = Student.objects.filter(school=request.user, serial=serial)[0]
	blank_warning = []

	if not student.f_name or student.f_name == '':
		blank_warning.append('Father\'s Name is BLANK')

	if not student.m_name or student.m_name == '':
		blank_warning.append('Mother\'s Name is BLANK')

	if (student.f_name == '' or student.f_name is None) and (student.g_indicator == '' or student.g_indicator is None):
		if (student.m_name == '' or not student.m_name) and (student.f_name == '' or not student.f_name):
			if not student.g_name or student.g_name == '':
				blank_warning.append('Guardian\'s Name is BLANK')

	if not student.dob or student.dob == '':
		blank_warning.append('Date of Birth is BLANK')

	if student.name == student.f_name:
		blank_warning.append('Candidate Name and Father\'s Name are SAME')

	if student.name == student.m_name:
		blank_warning.append('Candidate Name and Mother\'s Name are SAME')

	if (student.m_name == student.f_name) and (student.m_name or student.f_name):
		blank_warning.append('Mother\'s Name and Father\'s Name are SAME')

	context = {
		'student': student,
		'blank_warning': blank_warning

	}
	return render(request, 'student/student.html', context)

@login_required
@can_edit_data
def select_student(request, serial):
	try:
		profile = request.user.profile
		pass
	except Profile.DoesNotExist:
		return redirect('school:profile')

	student = Student.objects.filter(school=request.user, serial=serial)[0]
	dob = student.dob

	extra_warning = ''

	if (not student.f_name and not student.m_name and student.g_name) or (student.f_name == '' and student.m_name == '' and student.g_name):
		extra_warning = 'Warning! Father\'s Name and Mother\'s Name are blank. '


	if (not student.f_name and not student.m_name and not student.g_name) or (student.f_name == '' and student.m_name == '' and student.g_name == ''):
		messages.error(request, f'Student with \"Blank Father\'s Name, Mother\'s Name or Guardian\'s Name\",  {student.name} can not be selected.')
		return redirect(student.get_absolute_url())


	elif not dob or dob == '':
		messages.error(request, f'Student with \"Blank Date of Birth\",  {student.name} can not be selected.')
		return redirect(student.get_absolute_url())

	elif datetime.strptime(dob, '%d%m%y') and datetime.strptime(dob, '%d%m%y') > datetime.strptime('311007', '%d%m%y'):
		messages.error(request, f'Under-Age Student,  {student.name} can not be selected.')
		return redirect(student.get_absolute_url())

	student.status = '1'
	student.save()

	try:
		next_student = Student.objects.filter(school=request.user, serial__gt=serial).first()
		messages.success(request, f'{extra_warning}Student {student.name} has been marked as Selected.')
		return redirect(next_student.get_absolute_url())
	except Exception:
		return redirect('school:student_list')

@login_required
@can_edit_data
def not_select_student(request, serial):
	try:
		profile = request.user.profile
		pass
	except Profile.DoesNotExist:
		return redirect('school:profile')

	student = Student.objects.filter(school=request.user, serial=serial)[0]
	extra_warning = ''

	if (not student.f_name and not student.m_name and student.g_name) or (student.f_name == '' and student.m_name == '' and student.g_name):
		extra_warning = 'Warning! Father\'s Name and Mother\'s Name are blank. '

	student.status = '2'
	student.save()


	try:
		next_student = Student.objects.filter(school=request.user, serial__gt=serial).first()
		messages.warning(request, f'{extra_warning}Student {student.name} has been marked as NOT Selected')
		return redirect(next_student.get_absolute_url())
	except Exception:
		return redirect('school:student_list')

@login_required
@can_edit_data
def edit_student(request, serial):
	try:
		profile = request.user.profile
		pass
	except Profile.DoesNotExist:
		return redirect('school:profile')
		
	student = Student.objects.filter(school=request.user, serial=serial)[0]
	student_dict = model_to_dict(student, fields=[field.name for field in student._meta.fields])
	student_dict['g_name'] = student.get_guardian_name()
	try:
		student_dict['dob'] = datetime.strptime(student_dict['dob'], '%d%m%y')
	except (ValueError, KeyError, TypeError):
		student_dict['dob'] = ''
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
			try:
				dob = form.cleaned_data.get('dob').strftime('%d%m%y')
			except AttributeError:
				dob = None
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