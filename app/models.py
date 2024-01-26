from django.db import models

# Create your models here.


class BookHolder(models.Model):
    name = models.CharField(max_length=50)
