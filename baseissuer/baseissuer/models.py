from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import AbstractUser

from simple_email_confirmation import SimpleEmailConfirmationUserMixin

class BaseIssuerManager(BaseUserManager):

    def create_user(self, email, password=None):
        if not email:
            msg = "Issuers must have an email address"
            raise ValueError(msg)

        issuer = self.model(email=BaseIssuerManager.normalize_email(email))
        issuer.set_password(password)
        issuer.save(using=self._db)
        return issuer

    def create_superuser(self, email, password):
        issuer = self.create_user(email=email, password=password)
        issuer.is_confirmed = True
        issuer.save(using=self._db)
        return issuer


class BaseIssuer(SimpleEmailConfirmationUserMixin, AbstractBaseUser):

    # Basic information
    email = models.EmailField(verbose_name="Email Address", max_length=255,
                              unique=True, db_index=True)
    name = models.CharField(unique=True, max_length=20)
    url = models.URLField()

    update_time = models.DateTimeField(auto_now=True)
    create_time = models.DateTimeField(auto_now_add=True)
    
    is_active = models.BooleanField(default=False)
    is_confirm = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    objects = BaseIssuerManager()

    class Meta:
        verbose_name = 'issuer'

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.name

    def __str__(self):
        return self.email


class Address(models.Model):
    address = models.CharField(primary_key=True, max_length=50)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

class Color(models.Model):
    color_id = models.BigIntegerField(primary_key=True)
    color_name = models.CharField(unique=True, max_length=50)
    issuer = models.ForeignKey(BaseIssuer)
    address = models.OneToOneField(Address)

    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    is_confirmed = models.BooleanField(default=False)
