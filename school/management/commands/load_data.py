from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

import csv
import time

from student.models import Student

def get_profile_pic_path(data):
    if data['profile_pic_ind'].lower() == 'y':
        path_target = data['path_target']
        split_paths = path_target.split('\\')
        filename = split_paths[1].split('.')[0].lower()
        return f'{split_paths[0]}/{filename}_t1.JPG'
    elif data['profile_pic_ind'].lower() == 'z':
        path_target = data['path_target']
        split_paths = path_target.split('\\')
        filename = split_paths[1].split('.')[0].lower()
        return f'{split_paths[0]}/{filename}.JPG'
    return None

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
                    school_id = User.objects.get(username=row['school_username']).id
                    row['school_id'] = school_id
                    row['profile_picture'] = get_profile_pic_path(row)
                    row.pop('school_username')

                    print(f"\033[0mLoading Student {row['school_id']} - {row['serial']}")
                    students.append(Student(**row))
                csv_file.close()

            Student.objects.bulk_create(students)
            print('\033[1;32m-'*21)
            print('\033[1;32mStudent objects created!')
            print('\033[1;32m-'*21)
