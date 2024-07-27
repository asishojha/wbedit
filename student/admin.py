from django.contrib import admin
from .models import Student, SupportDocument


class StudentAdmin(admin.ModelAdmin):
    pass


class SupportDocumentAdmin(admin.ModelAdmin):
    pass


admin.site.register(Student, StudentAdmin)
admin.site.register(SupportDocument, SupportDocumentAdmin)
