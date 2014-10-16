from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Polis(models.Model):
    name = models.CharField(unique=True, max_length=30)
    register_url = models.URLField()
    update_time = models.DateTimeField(auto_now=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Poleis'

class Color(models.Model):
    color_number = models.BigIntegerField(primary_key=True)
    polis = models.ForeignKey(Polis)

class PolisOwner(models.Model):
    user = models.OneToOneField(User)
    polis = models.ForeignKey(Polis)
    
    def __str__(self):
        return self.user.username + " " + self.polis.name


    def delete(self, *args, **kwargs):
        self.user.delete()
        self.polis.delete()
        super(PolisOwner, self).delete(*args, **kwargs)


    def deactive(self):
        self.user.is_active = False
        self.user.save()

    def active(self):
        self.user.is_active = True
        self.user.save()

    def is_active(self):
        return self.user.is_active


