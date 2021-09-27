from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from weasyprint import HTML
import tempfile

def download_pdf(school):
	html_string = render_to_string('school/pdf-report.html', {'school': school})
	html = HTML(string=html_string)
	result = html.write_pdf()

	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'inline; filename="{}.pdf"'.format(school.username)
	response['Content-Transfer-Encoding'] = 'binary'

	with tempfile.NamedTemporaryFile(delete=True) as output:
		output.write(result)
		output.flush()
		output = open(output.name, 'r')
		response = write(output.read())

	return response