from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

import csv
import time

from student.models import Student


class Command(BaseCommand):
    help = 'Load data in database'

    def add_arguments(self, parser):
        parser.add_argument('-sc', '--schools', action='store_true',
                            help='Indicates wether to load data of schools')
        parser.add_argument('-st', '--students', action='store_true',
                            help='Indicates wether to load data of students')

    def handle(self, *args, **kwargs):
        load_schools = kwargs['schools']
        load_students = kwargs['students']

        if load_schools:
            users = []
            with open('SCH.CSV', 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    row['password'] = make_password('password')

                    print(f"\033[0mLoading school {row['username']}")
                    users.append(User(**row))
                csv_file.close()

            User.objects.bulk_create(users)
            print('\033[1;32m-'*16)
            print('\033[1;32mSchools created!')
            print('\033[1;32m-'*16)

            time.sleep(2)

        if load_students:
            students = []
            with open('STD.CSV', 'r') as csv_file:
                reader = csv.DictReader(csv_file)
                for row in reader:
                    print(row)
                    school_id = User.objects.get(username=row['school_username']).id
                    row.pop('school_username')
                    row['school_id'] = school_id
                    students.append(Student(**row))
                csv_file.close()

            Student.objects.bulk_create(students)
            print('\033[1;32m-'*21)
            print('\033[1;32mStudent objects created!')
            print('\033[1;32m-'*21)
