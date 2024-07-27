from django.shortcuts import redirect
from django.contrib import messages
from school.models import Profile


def can_edit_data(func):
    def wrap(request, *args, **kwargs):
        if not request.user.profile.complete:
            return func(request, *args, **kwargs)
        messages.warning(
            request,
            f"Final data for {request.user.username} has already been submitted. Please download the PDF report from below.",
        )
        return redirect("school:student_list")

    return wrap
