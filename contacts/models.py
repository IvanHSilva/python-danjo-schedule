from django.db import models
from django.utils import timezone

class Category(models.Model):
    catname = models.CharField(max_length=70)

    def __str__(self):
        return self.catname

class Contact(models.Model):
    id = models.IntegerField
    name = models.CharField(max_length=50)
    midname = models.CharField(max_length=50)
    phone = models.CharField(max_length=16)
    email = models.CharField(max_length=100, blank=True)
    createdate = models.DateTimeField(default=timezone.now)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING)
    active = models.BooleanField(default=True)
    photo = models.ImageField(blank=True, upload_to='pictures/%Y/%m/')

    def __str__(self):
        return self.name
