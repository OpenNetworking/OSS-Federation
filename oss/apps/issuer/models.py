from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Issuer(models.Model):
    user = models.OneToOneField(User)
    register_url = models.URLField()
    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)

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

class ActiveAddress(models.Model):
    """
    Address that used by Color currently.
    """
    address = models.CharField(primary_key=True, max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)

class Color(models.Model):
    color_number = models.BigIntegerField(primary_key=True)
    color_name = models.CharField(unique=True, max_length=50)
    issuer = models.ForeignKey(Issuer)
    current_address = models.OneToOneField(ActiveAddress)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

class HistoryAddress(models.Model):
    """
    Address has used by color in the past, and now is not using.
    This data can be used to trace transaction history.
    """
    address = models.CharField(primary_key=True, max_length=50)
    color = models.ForeignKey(Color)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(auto_now_add=True)


