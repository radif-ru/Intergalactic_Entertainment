import os

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Fill DB new data. Win Edition'

    def handle(self, *args, **options):
        os.system('del db.sqlite3')
        os.system('python manage.py makemigrations')
        os.system('python manage.py migrate')
        os.system('python manage.py fill_db')
        os.system('python manage.py runserver')
