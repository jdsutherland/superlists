import uuid

from django.db import models


class User(models.Model):
    email = models.EmailField(primary_key=True)
    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'
    is_anonymous = False
    is_authenticated = True

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email


class Token(models.Model):
    email = models.EmailField(max_length=75, blank=True)
    uid = models.CharField(default=uuid.uuid4, max_length=40)

    class Meta:
        verbose_name = "Token"
        verbose_name_plural = "Tokens"

    def __str__(self):
        return f'{self.email}: {self.uid}'