from django import template
from datetime import datetime

register = template.Library()

@register.filter(name='date_format')
def date_format(value):
	try:
		date = datetime.strptime(value, '%d%m%y')
		return date
	except (ValueError, KeyError, TypeError):
		return ''

@register.filter(name='index_format')
def index_format(value):
	return '-'.join([value[:2], value[2:]])