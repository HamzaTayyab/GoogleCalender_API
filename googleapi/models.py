from django.db import models
from django.db.models import JSONField

# Create your models here.


class teachers(models.Model):
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    calculations = models.BooleanField()
    clinical_pharmacy = models.BooleanField()
    pharmacy_law = models.BooleanField()
    compounding_exam = models.BooleanField()
    general_pharmacology = models.BooleanField()
    imagelink = models.CharField(max_length=250)
    credentials = models.TextField(null=True, blank=True)
