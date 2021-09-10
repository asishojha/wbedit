from django.urls import path
from .views import index, login_view, logout_view, student_list, submit_final_data, pdf_report, profile, reset_password

app_name = 'school'

urlpatterns = [
	path('', index, name='index'),
    path('login/', login_view, name = "login"),
    path('logout/', logout_view, name = "logout"),
    path('students/', student_list, name='student_list'),
    path('submit-data/', submit_final_data, name='submit_final_data'),
    path('pdf-report/', pdf_report, name='pdf_report'),
    path('profile/', profile, name='profile'),
    path('reset-password/', reset_password, name='reset_password'),
]