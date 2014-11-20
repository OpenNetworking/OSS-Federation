from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords

class Issuer(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(unique=True, max_length=20)
    url = models.URLField()
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return self.user.username

    def active(self):
        self.user.is_active = True
        self.user.save()

    def deactive(self):
        self.user.is_active = False
        self.user.save()

    def is_active(self):
        return self.user.is_active

    def delete(self, *args, **kwargs):
        self.user.delete()
        super(Issuer, self).delete(*args, **kwargs)

class Address(models.Model):
    address = models.CharField(primary_key=True, max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()

class Color(models.Model):
    color_id = models.BigIntegerField(primary_key=True)
    color_name = models.CharField(unique=True, max_length=50)
    issuer = models.ForeignKey(Issuer)
    address = models.ForeignKey(Address)
    is_confirmed = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    history = HistoricalRecords()
