from django.core.management.base import BaseCommand

from student.models import Student


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        students = Student.objects.filter(profile_pic_ind__iexact="z")
        exclusions = ["H1026", "V2015", "F2012"]
        for student in students:
            profile_picture = student.profile_picture
            name = profile_picture.name
            if any([exclusion in name for exclusion in exclusions]):
                continue
            extension = name.split(".")[-1]
            new_extension = extension.lower()
            new_name = name.replace(extension, new_extension)
            student.profile_picture.name = new_name
            student.save()
