from django import forms
from django.contrib.auth import authenticate
from .models import Profile

class UsersLoginForm(forms.Form):
	username = forms.CharField()
	password = forms.CharField(widget = forms.PasswordInput)
	
	def __init__(self, *args, **kwargs):
		super(UsersLoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update({
			'class': 'form-control',
			"name":"username"})
		self.fields['password'].widget.attrs.update({
			'class': 'form-control',
			"name":"password"})

	def clean(self, *args, **keyargs):
		username = self.cleaned_data.get("username")
		password = self.cleaned_data.get("password")
		if username and password:
			user = authenticate(username = username, password = password)
			if not user:
				raise forms.ValidationError("Invalid Credentials! Please check username and password again.")
			if not user.is_active:
				raise forms.ValidationError("User is no longer active")
			
		return super(UsersLoginForm, self).clean(*args, **keyargs)

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		exclude = ['school', 'complete']

	def __init__(self, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)
		
		self.fields['headmaster_name'].label = 'Name of H.M. / T.I.C'      
		self.fields['headmaster_phone'].label = 'Mobile Number'
		self.fields['headmaster_email'].label = 'E-mail Address'

		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control'})