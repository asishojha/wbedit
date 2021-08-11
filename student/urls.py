from django.urls import path
from .views import student, select_student, not_select_student, edit_student

app_name = 'student'

urlpatterns = [
	path('<slug:serial>/', student, name='student'),
	path('select-student/<slug:serial>/', select_student, name='select_student'),
	path('not-select-student/<slug:serial>/', not_select_student, name='not_select_student'),
	path('edit-student/<slug:serial>/', edit_student, name='edit_student'),
]