from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from school.models import Profile

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
	"24":"HISTORY",
	"25":"GEOGRAPHY",
	"26":"MATHEMATICS",
	"27":"PHYSICAL SCIENCE",
	"28":"LIFE SCIENCE",
	"31":"BENGALI(A LEVEL)",
	"32":"ENGLISH",
	"33":"HINDI(A LEVEL)",
	"34":"NEPALI",
	"35":"URDU",
	"36":"BENGALI(B LEVEL)",
	"37":"SANSKRIT",
	"38":"PALI",
	"39":"PERSIAN",
	"40":"ARABIC",
	"41":"LATIN",
	"42":"GREEK",
	"43":"CLASSICAL TIBETAN",
	"44":"FRENCH",
	"45":"GERMAN",
	"46":"RUSSIAN",
	"47":"HINDI(B LEVEL)",
	"48":"PORTUGUESE",
	"49":"SPANISH",
	"50":"ITALIAN",
	"51":"CLASSICAL ARMENIAN",
	"52":"MATHEMATICS",
	"53":"BUILDING MATERIAL & CONST",
	"54":"PHYSICS",
	"55":"CHEMISTRY",
	"56":"BIOLOGY",
	"57":"MECHANICS",
	"58":"GEOGRAPHY",
	"59":"WORLD HISTORY",
	"60":"LOGIC",
	"61":"PSYCHOLOGY",
	"62":"BUSINESS METHOD & CORRESPONDENCE",
	"63":"BOOK KEEPING",
	"64":"EL.OF ECONOMICS & CIVICS",
	"65":"HOME SC. AND HOME NURSING",
	"66":"MUSIC VOCAL",
	"67":"MUSIC INSTRUMENTAL",
	"68":"EL.OF INDIAN ART",
	"69":"WOOD WORK & WORK -SHOP TECHNOLOGY",
	"70":"SEWING AND NEEDLE CRAFT",
	"71":"EL.OF AGRL. AND HORTICULTURE",
	"72":"PISCICULTURE",
	"73":"ANIMAL HUSBANDRY /POULTRY FARM",
	"74":"SHORTHAND AND TYPE WRITING",
	"75":"EL.OF GEN.ENGG. KNOWLEDGE",
	"76":"PHYSIOLOGY & HYGIENE",
	"81":"WORK EDUCATION",
	"82":"PHYSICAL EDUCN.",
	"83":"SOCIAL SERVICE",
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

	def get_guardian_name(self):
		if self.g_indicator == 'M':
			return self.m_name
		if self.g_indicator == '' and self.g_name == '':
			return self.f_name
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