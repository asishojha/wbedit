from django.urls import path
from .views import index, login_view, logout_view, student_list, submit_final_data

app_name = 'school'

urlpatterns = [
	path('', index, name='index'),
    path('login/', login_view, name = "login"),
    path('logout/', logout_view, name = "logout"),
    path('students/', student_list, name='student_list'),
    path('submit-data/', submit_final_data, name='submit_final_data'),
]