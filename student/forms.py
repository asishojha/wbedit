from django import forms
from .models import Student, SupportDocument
from django.utils.translation import gettext_lazy as _

FIRST_LANGUAGE_CODE = (
	('02', 'BENGALI'),
	('03', 'ENGLISH'),
	('04', 'GUJRATI'),
	('05', 'HINDI'),
	('09', 'MODERN TIBETAN'),
	('10', 'NEPALI'),
	('11', 'ODIA'),
	('12', 'GURUMUKHI(PUNJABI)'),
	('13', 'SANTALI'),
	('15', 'TELEGU'),
	('16', 'TAMIL'),
	('17', 'URDU')
)

SECOND_LANGUAGE_CODE = (
	('21', 'ENGLISH'),
	('22', 'BENGALI'),
	('23', 'NEPALI')
)

OPTIONAL_ELECTIVE_CODE = (
	("", "None"),
	("00",  "POWER"),
	("31", "BENGALI(A LEVEL)"),
	("32", "ENGLISH"),
	("33", "HINDI(A LEVEL)"),
	("34", "NEPALI"),
	("35", "URDU"),
	("36", "BENGALI(B LEVEL)"),
	("37", "SANSKRIT"),
	("47", "HINDI(B LEVEL)"),
	("52", "MATHEMATICS"),
	("53", "BUILDING MATERIAL & CONST"),
	("54", "PHYSICS"),
	("55", "CHEMISTRY"),
	("56", "BIOLOGY"),
	("57", "MECHANICS"),
	("58", "GEOGRAPHY"),
	("59", "WORLD HISTORY"),
	("60", "LOGIC"),
	("61", "PSYCHOLOGY"),
	("62", "BUSINESS METHOD & CORRESPONDENCE"),
	("63", "BOOK KEEPING"),
	("64", "EL.OF ECONOMICS & CIVICS"),
	("65", "HOME SC. AND HOME NURSING"),
	("66", "MUSIC VOCAL"),
	("67", "MUSIC INSTRUMENTAL"),
	("68", "EL.OF INDIAN ART"),
	("69", "WOOD WORK & WORK -SHOP TECHNOLOGY"),
	("70", "SEWING AND NEEDLE CRAFT"),
	("71", "EL.OF AGRL. AND HORTICULTURE"),
	("72", "PISCICULTURE"),
	("73", "ANIMAL HUSBANDRY /POULTRY FARM"),
	("74", "SHORTHAND AND TYPE WRITING"),
	("75", "EL.OF GEN.ENGG. KNOWLEDGE"),
	("76", "PHYSIOLOGY & HYGIENE"),
	("81", "WORK EDUCATION"),
	("82", "PHYSICAL EDUCN."),
	("83", "SOCIAL SERVICE"),
	("84", "WORK EDUCATION GROUP"),
	("85", "COMPUTER APPLICATION"),
	("86", "RETAIL SECTOR"),
	("87", "SECURITY SECTOR"),
	("88", "AUTOMOBILE SECTOR"),
	("89", "IT/IT'es SECTOR"),
	("90", "HEALTH CARE SECTOR"),
	("91", "ELECTRONICS"),
	("92", "IRON & STEEL"),
	("93", "TOURISM & HOSPITALITY"),
	("94", "CONSTRUCTION"),
	("95", "APPAREL"),
	("96", "PLUMBING"),
	("97", "BEAUTY & WELLNESS"),
	("98", "LEATHER"),
	("99", "AGRICULTURE")
)

CASTE_CHOICES = (
	("", "GENERAL"),
	("1", "SCHEDULED CASTE"),
	("2", "SCHEDULED TRIBES"),
	("3", "OTHER BACKWARD CLASSES")
)

RELIGION_CHOICES = (
	("1", "HINDUISM"),
	("2", "ISLAM"),
	("3", "CHRISTIANITY"),
	("4", "BUDDHISM"),
	("5", "SIKHISM"),
	("6", "ZORASTRIAN"),
	("7", "OTHERS"),
)

SEX_CHOICES = (
	("1", "MALE"),
	("2", "FEMALE")
)

class StudentForm(forms.ModelForm):
	fl = forms.ChoiceField(choices=FIRST_LANGUAGE_CODE, label='First Language')
	sl = forms.ChoiceField(choices=SECOND_LANGUAGE_CODE, label='Second Language')
	opt = forms.ChoiceField(choices=OPTIONAL_ELECTIVE_CODE, label='Optional Elective', required=False)
	caste = forms.ChoiceField(choices=CASTE_CHOICES, required=False)
	religion = forms.ChoiceField(choices=RELIGION_CHOICES)
	sex = forms.ChoiceField(choices=SEX_CHOICES, label='Gender')
	dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Date of Birth')
	edited = forms.CharField(widget=forms.HiddenInput)
	document = forms.CharField(max_length=50, help_text='Please mention the supporting document on basis of which the change was made. Ex: admission register / birth certificate / etc', required=False)

	class Meta:
		model = Student
		exclude = ['school', 'school_profile', 'path_target', 'serial', 'dob_edited', 'selected', 'not_selected', 'g_indicator', 'status']

	def __init__(self, *args, **kwargs):
		super(StudentForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control mb-3'})

	def clean(self, *args, **kwargs):
		cleaned_data = self.cleaned_data
		fl = cleaned_data.get('fl')
		sl = cleaned_data.get('sl')

		if fl == '02' and sl == '22':
			raise forms.ValidationError(
				_('Invalid FL and SL combination'),
				code='invalid'
				)
		if fl == '03' and sl != '22':
			raise forms.ValidationError(
				_('Invalid FL and SL combination'),
				code='invalid'
				)
		if fl == '10' and sl == '23':
			raise forms.ValidationError(
				_('Invalid FL and SL combination'),
				code='invalid'
				)
		return cleaned_data

# class SupportDocumentForm(forms.ModelForm):
# 	class Meta:
# 		model = SupportDocument
# 		exclude = ['student']

# 	def __init__(self, *args, **kwargs):
# 		super(SupportDocumentForm, self).__init__(*args, **kwargs)
# 		for field in self.fields:
# 			self.fields[field].widget.attrs.update({'class': 'form-control mb-3'})