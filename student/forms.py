from django import forms
from .models import Student

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
    ("00",  "POWER"),
    ("24", "HISTORY"),
    ("25", "GEOGRAPHY"),
    ("26", "MATHEMATICS"),
    ("27", "PHYSICAL SCIENCE"),
    ("28", "LIFE SCIENCE"),
    ("31", "BENGALI(A LEVEL)"),
    ("32", "ENGLISH"),
    ("33", "HINDI(A LEVEL)"),
    ("34", "NEPALI"),
    ("35", "URDU"),
    ("36", "BENGALI(B LEVEL)"),
    ("37", "SANSKRIT"),
    ("38", "PALI"),
    ("39", "PERSIAN"),
    ("40", "ARABIC"),
    ("41", "LATIN"),
    ("42", "GREEK"),
    ("43", "CLASSICAL TIBETAN"),
    ("44", "FRENCH"),
    ("45", "GERMAN"),
    ("46", "RUSSIAN"),
    ("47", "HINDI(B LEVEL)"),
    ("48", "PORTUGUESE"),
    ("49", "SPANISH"),
    ("50", "ITALIAN"),
    ("51", "CLASSICAL ARMENIAN"),
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
	opt = forms.ChoiceField(choices=OPTIONAL_ELECTIVE_CODE, label='Optional Elective')
	caste = forms.ChoiceField(choices=CASTE_CHOICES, required=False)
	religion = forms.ChoiceField(choices=RELIGION_CHOICES)
	sex = forms.ChoiceField(choices=SEX_CHOICES, label='Gender')
	dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Date of Birth')

	class Meta:
		model = Student
		exclude = ['school', 'school_profile', 'path_target', 'serial', 'edited', 'dob_edited', 'selected', 'not_selected', 'g_indicator']

	def __init__(self, *args, **kwargs):
		super(StudentForm, self).__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({'class': 'form-control mb-3'})