from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class fileModel(models.Model):
    file = models.FileField(upload_to='uploads/')

class Month(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET("deleted user"), null=True)
    name = models.CharField(max_length=30)
    created = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True,blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name

class Entry(models.Model):
    creator = models.ForeignKey(User, on_delete=models.SET("deleted user"), null= True)
    month = models.ForeignKey(Month, on_delete=models.CASCADE, null= True) 
    date = models.CharField(max_length=10)
    concepto = models.TextField(null=True, blank=True)
    cargo = models.CharField(max_length=100,null= True,blank= True)
    abono = models.CharField(max_length=100,null= True,blank= True)
    saldo = models.CharField(max_length=100,null= True,blank= True)
    description = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} :{self.description}"


