

from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class User(AbstractUser):
    is_admin = models.BooleanField()
    is_librarian = models.BooleanField()
    is_library_staff = models.BooleanField(null=True)


class LibrarianModel(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE
    )

    dob = models.DateField(null=True)
    gender = models.CharField(max_length=12, null=True)
    profile_image = models.ImageField(
        null=True, upload_to="profile_image", blank=True)
    slug = models.SlugField(null=True, unique=True)


class LibrarystaffProfileModel(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
    )
    slug = models.SlugField(null=True, unique=True)
    staff_profile_image = models.ImageField(
        null=True, upload_to="staff_profile_image", blank=True)
    is_active = models.BooleanField(default=True)
    dob = models.DateField(null=True)
    gender = models.CharField(max_length=12)
    senior_staff = models.ForeignKey(
        LibrarianModel, on_delete=models.CASCADE, null=True
    )


class BookCategoryModel(models.Model):
    slug = models.SlugField(null=True, unique=True)
    is_active = models.BooleanField(default=True)
    manager = models.ForeignKey(
        LibrarystaffProfileModel, on_delete=models.CASCADE
    )
    librarian = models.OneToOneField(
        LibrarianModel, on_delete=models.CASCADE
    )
    label = models.CharField(max_length=20)
    description = models.CharField(max_length=50)


class PublisherModel(models.Model):
    slug = models.SlugField(null=True, unique=True)
    is_active = models.BooleanField(default=True)
    label = models.CharField(max_length=50)
    description = models.CharField(max_length=50)


class BookModel(models.Model):
    slug = models.SlugField(null=True, unique=True)
    is_active = models.BooleanField(default=True)
    label = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    publisher = models.ForeignKey(
        PublisherModel, on_delete=models.CASCADE
    )
    category = models.ManyToManyField(
        BookCategoryModel
    )
