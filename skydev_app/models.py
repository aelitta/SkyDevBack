from django.db import models

# Create your models here.
class Domain(models.Model):
    name = models.CharField(max_length=255)
    value = models.CharField(max_length=255)
    code = models.IntegerField()