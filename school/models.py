from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Profile(models.Model):
	school = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
	headmaster_name = models.CharField(max_length=50)
	headmaster_email = models.EmailField(max_length=70)
	headmaster_phone = models.BigIntegerField(validators=[MinValueValidator(1000000000), MaxValueValidator(9999999999)])
	created_on = models.DateTimeField(auto_now_add=True)
	modified_on = models.DateTimeField(auto_now=True)
	complete = models.BooleanField(default=False)
	password_changed = models.BooleanField(default=False)
	verification_name = models.CharField(max_length=50, null=True)

	def __str__(self):
		return self.school.username