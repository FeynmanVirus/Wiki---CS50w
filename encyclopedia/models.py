from django.db import models

# Create your models here.
class WForm(models.Model):
    title = models.CharField(max_length=100, verbose_name="")
    content = models.CharField(max_length=1000000, verbose_name="")
