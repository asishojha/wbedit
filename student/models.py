from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from school.models import Profile

SUBJECT_SHORT_CODE = {
	"00": "Pwr",
	"01":"AS",
	"02":"B(FL)",
	"03":"E(FL)",
	"04":"GUJ(FL)",
	"05":"HIN(FL)",
	"06":"MAL(FL)",
	"07":"MAR(FL)",
	"08":"LU(FL)",
	"09":"TBM(FL)",
	"10":"N(FL)",
	"11":"OY(FL)",
	"12":"GUR(FL)",
	"13":"SAN(FL)",
	"14":"SAD(FL)",
	"15":"TEL(FL)",
	"16":"TAM(FL)",
	"17":"U(FL)",
	"20":"E(SL)",
	"21":"E(SL)",
	"22":"B(SL)",
	"23":"N(SL)",
	"31":"B(A)",
	"32":"E",
	"33":"HIN(A)",
	"34":"N",
	"35":"U",
	"36":"B(B)",
	"37":"S",
	"47":"HIN(B)",
	"52":"M",
	"54":"PH",
	"55":"CH",
	"56":"BIO",
	"57":"MC",
	"58":"G",
	"60":"LG",
	"61":"PSY",
	"62":"BC",
	"63":"BK",
	"64":"EC",
	"65":"HS",
	"66":"MU V",
	"67":"MU I",
	"70":"SEW",
	"71":"AG",
	"72":"PS",
	"73":"AH",
	"76":"HY",
	"84":"WPS",
	"85":"CA",
	"86":"RStr",
	"87":"SStr",
	"88":"AStr",
	"89":"IT",
	"90":"HStr",
	"91":"Elec",
	"92":"IS",
	"93":"TH",
	"94":"Cons",
	"95":"Aprl",
	"96":"Plmb",
	"97":"BW",
	"98":"Lthr",
	"99": "Agrl"
}

FIRST_LANGUAGE_CODE = {
	'02':'BENGALI',
	'03':'ENGLISH',
	'04':'GUJRATI',
	'05':'HINDI',
	'09':'MODERN TIBETAN',
	'10':'NEPALI',
	'11':'ODIA',
	'12':'GURUMUKHI(PUNJABI)',
	'13':'SANTALI',
	'15':'TELEGU',
	'16':'TAMIL',
	'17':'URDU'
}

SECOND_LANGUAGE_CODE = {
	'21':'ENGLISH',
	'22':'BENGALI',
	'23':'NEPALI'
}

OPTIONAL_ELECTIVE_SUBJECTS_DICT = {
	"00": "POWER",
	"31":"BENGALI(A LEVEL)",
	"32":"ENGLISH",
	"33":"HINDI(A LEVEL)",
	"34":"NEPALI",
	"35":"URDU",
	"36":"BENGALI(B LEVEL)",
	"37":"SANSKRIT",
	"47":"HINDI(B LEVEL)",
	"52":"MATHEMATICS",
	"54":"PHYSICS",
	"55":"CHEMISTRY",
	"56":"BIOLOGY",
	"57":"MECHANICS",
	"58":"GEOGRAPHY",
	"60":"LOGIC",
	"61":"PSYCHOLOGY",
	"62":"BUSINESS METHOD & CORRESPONDENCE",
	"63":"BOOK KEEPING",
	"64":"EL.OF ECONOMICS & CIVICS",
	"65":"HOME SC. AND HOME NURSING",
	"66":"MUSIC VOCAL",
	"67":"MUSIC INSTRUMENTAL",
	"70":"SEWING AND NEEDLE CRAFT",
	"71":"EL.OF AGRL. AND HORTICULTURE",
	"72":"PISCICULTURE",
	"73":"ANIMAL HUSBANDRY /POULTRY FARM",
	"76":"PHYSIOLOGY & HYGIENE",
	"84":"WORK EDUCATION GROUP",
	"85":"COMPUTER APPLICATION",
	"86":"RETAIL SECTOR",
	"87":"SECURITY SECTOR",
	"88":"AUTOMOBILE SECTOR",
	"89":"IT/IT'es SECTOR",
	"90":"HEALTH CARE SECTOR",
	"91":"ELECTRONICS",
	"92":"IRON & STEEL",
	"93":"TOURISM & HOSPITALITY",
	"94":"CONSTRUCTION",
	"95":"APPAREL",
	"96":"PLUMBING",
	"97":"BEAUTY & WELLNESS",
	"98":"LEATHER",
	"99": "AGRICULTURE"
}

RELIGION_DICT = {
	"1": "HINDUISM",
	"2": "ISLAM",
	"3": "CHRISTIANITY",
	"4": "BUDDHISM",
	"5": "SIKHISM",
	"6": "ZORASTRIAN",
	"7": "OTHERS",
}

CASTE_DICT = {
	"": "GENERAL",
	"1": "SCHEDULED CASTE",
	"2": "SCHEDULED TRIBES",
	"3": "OTHER BACKWARD CLASSES"
}

SEX_CHOICES = {
	"1": "MALE",
	"2": "FEMALE"
}

STATUS_CHOICES = (
	('', 'Pending'),
	('1', 'Selected'),
	('2', 'Not Selected'),
)

class Student(models.Model):
	school = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
	school_profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
	path_target = models.CharField(max_length=20)
	name = models.CharField(max_length=40)
	f_name = models.CharField(max_length=40, verbose_name='Father\'s Name', null=True, blank=True)
	m_name = models.CharField(max_length=40, verbose_name='Mother\'s Name', null=True, blank=True)
	g_indicator = models.CharField(max_length=1, null=True, blank=True)
	g_name = models.CharField(max_length=40, null=True, verbose_name='Guardian\'s Name', blank=True)
	sex = models.CharField(max_length=1, verbose_name='Gender')
	religion = models.CharField(max_length=1)
	caste = models.CharField(max_length=1, null=True, blank=True)
	dob = models.CharField(max_length=10, verbose_name='Date of Birth')
	fl = models.CharField(max_length=2, verbose_name='First Language')
	sl = models.CharField(max_length=2, verbose_name='Second Language')
	opt = models.CharField(max_length=2, null=True, blank=True, verbose_name='Optional Elective')
	serial = models.CharField(max_length=4)
	edited = models.BooleanField(default=False)
	status = models.CharField(max_length=1, choices=STATUS_CHOICES, null=True)

	def __str__(self):
		return self.school.username

	def get_absolute_url(self):
		return reverse('student:student' , kwargs={
			'serial' : self.serial
		})

	def get_fl_name(self):
		return FIRST_LANGUAGE_CODE[self.fl]

	def get_sl_name(self):
		return SECOND_LANGUAGE_CODE[self.sl]

	def get_opt_name(self):
		if self.opt:
			return OPTIONAL_ELECTIVE_SUBJECTS_DICT[self.opt]
		return ""

	def get_fl_short_code(self):
		return SUBJECT_SHORT_CODE[self.fl]

	def get_sl_short_code(self):
		return SUBJECT_SHORT_CODE[self.sl]

	def get_opt_el_short_code(self):
		if self.opt:
			return SUBJECT_SHORT_CODE[self.opt]
		return ""

	def get_guardian_name(self):
		if self.g_indicator == 'M':
			if self.g_name == '':
				return self.m_name
			elif self.g_name == self.f_name:
				return self.f_name
			else:
				return self.g_name
		else:
			if self.g_name == self.m_name:
				return self.m_name
			elif self.g_name == self.f_name:
				return self.f_name
			elif self.g_name == '':
				return self.f_name
			else:
				return self.g_name

	def get_gender(self):
		return SEX_CHOICES[self.sex]

	def get_caste(self):
		if self.caste:
			return CASTE_DICT[self.caste]
		return 'GENERAL'

	def get_religion(self):
		return RELIGION_DICT[self.religion]
		
	class Meta:
		ordering = ('serial', )

	def save(self, *args, **kwargs):
		self.name = self.name.upper()
		self.f_name = self.f_name.upper()
		self.m_name = self.m_name.upper()
		self.g_name = self.g_name.upper()
		super(Student, self).save(*args, **kwargs)

class SupportDocument(models.Model):
	student = models.OneToOneField(Student, on_delete=models.SET_NULL, null=True)
	document = models.CharField(max_length=50, help_text='Please mention the supporting document on basis of which the change was made. Ex: admission register / birth certificate / etc')

	def __str__(self):
		return self.student.serial