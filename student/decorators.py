from django.shortcuts import redirect
from django.contrib import messages
from school.models import Profile

def can_edit_data(func):
	def wrap(request, *args, **kwargs):
		if not request.user.profile.complete:
			return func(request, *args, **kwargs)
		messages.warning(request, f'Dear {request.user.username}, you have already submitted the final data. Please download the PDF report from below.')
		return redirect('school:student_list')
	return wrap