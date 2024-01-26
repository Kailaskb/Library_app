from datetime import date

from rest_framework.test import APITestCase

from app.models import BookHolder
from main.models import LibrarianModel
from main.views import Token, User

# Create your tests here.


class BasicTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.base_url = 'http://127.0.0.1:8000/bookholder/'

    def get_or_create_librarian(self):
        user = User.objects.filter(email='email@mail.com')
        if not user.exists():
            user = User.objects.create_user(
                        first_name='first_name',
                        last_name='last_name',
                        email='email@mail.com',
                        username='username',
                        password='password',    
                        is_admin=False,
                        is_librarian=True,
                        is_library_staff=False,
                        is_active=True,
                    )
            librarian = LibrarianModel.objects.create(
                user=user,
                gender='gender',
                dob=date.today(),
                profile_image='',
                
            )    
            return (user, librarian)
        user=user.first()
        librarian=LibrarianModel.objects.filter(user=user)
        return (user, librarian)

    def get_or_create_bookholder(self):
        user = BookHolder.objects.create(
            name="name"
        )
        return (user)
    def get_or_create_token(self,user):
        tokens=Token.objects.create(user=user)
        return (str(tokens.key))
    
    def get_or_create_librarian_token(self):
        (librarian)=self.get_or_create_librarian()
        return self.get_or_create_token(librarian[0]) 
    

