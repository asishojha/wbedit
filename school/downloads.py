from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from weasyprint import HTML

def download_pdf(school):
	html_string = render_to_string('school/pdf-report.html', {'school': school})
	html = HTML(string=html_string)
	html.write_pdf("pdfs/{}.pdf".format(school.username));
	return None