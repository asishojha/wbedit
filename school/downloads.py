from django.http import HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from weasyprint import HTML

schools = User.objects.exclude(is_superuser=True)
for school in schools:
    html_string = render_to_string("school/pdf-report.html", {"school": school})
    html = HTML(string=html_string)
    html.write_pdf("pdfs/{}.pdf".format(school.username))
    print("Downloading PDF for school", school.username)
