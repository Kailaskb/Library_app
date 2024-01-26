from getpass import getpass
from operator import truediv
from unittest import result

from django.core.management.base import BaseCommand
from main.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:

            username = input(' enter user name: ')
            email = input(' enter email: ')
            password = getpass(' enter your password: ')
            confirm_password = getpass(' re-enter your password: ')
            is_admin = True,
            is_librarian = False
            is_superuser = True
            if not password == confirm_password:
                print('password doet not match')
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_admin=True,
                is_librarian=False,
                is_superuser=True
            )
            print('admin created')

        except Exception as e:
            print(str(e))
