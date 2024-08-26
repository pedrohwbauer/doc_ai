from django.db import models

# Create your models here.
class Document(models.Model):
    title = models.CharField(max_length=80)
    file = models.FileField(upload_to='documents')