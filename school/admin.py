from django.contrib import admin, messages
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Permission
from django.utils.decorators import method_decorator
from django.urls import path, reverse

from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ["school__username"]

    @method_decorator(staff_member_required)
    def reset_password(self, request, pk):
        profile = Profile.objects.get(pk=pk)
        user = profile.school
        user.password = make_password("password")
        user.save()

        password_change_permission = Permission.objects.get(
            codename="can_change_password"
        )
        user.user_permissions.add(password_change_permission)

        messages.success(
            request,
            f"Password of the school with index {user.username} has been reset to 'password'.",
        )
        return redirect(
            reverse(
                "admin:%s_%s_change"
                % (self.model._meta.app_label, self.model._meta.model_name),
                args=(pk,),
            )
        )

    def get_urls(self):
        super_urls = super().get_urls()
        urls = [
            path(
                "<int:pk>/reset-password/",
                self.admin_site.admin_view(self.reset_password),
                name="reset_password",
            )
        ]
        return urls + super_urls


admin.site.register(Profile, ProfileAdmin)
