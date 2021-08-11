from django import template
from datetime import datetime

register = template.Library()

@register.filter(name='date_format')
def date_format(value):
	return datetime.strptime(value, '%d%m%y')