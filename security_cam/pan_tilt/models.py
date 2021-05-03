from django.db import models

# Create your models here.
class Coordinates(models.Model):
    sessionkey = models.CharField(max_length=100, default='')