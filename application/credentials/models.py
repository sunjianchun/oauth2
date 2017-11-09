from __future__ import unicode_literals

from django.db import models
from django.core.validators import EmailValidator, ValidationError
from application.credentials import pwd_context

class OAuthCredentials(models.Model):
    password = models.CharField(max_length=160)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.pk == None:
            self.password = pwd_context.encrypt(secret=self.password)
        elif not pwd_context.identify(hash=self.password):
            self.password = pwd_context.encrypt(secret=self.password)

        super(OAuthCredentials, self).save(*args, **kwargs)

    def verify_password(self, raw_password):
        return pwd_context.verify(secret=raw_password, hash=self.password)

class OAuthUser(OAuthCredentials):
    email = models.CharField(
        max_length=254,
        unique=True,
        validators=[EmailValidator()],
    )

    def __unicode__(self):
        return self.email


class OAuthClient(OAuthCredentials):
    client_id = models.CharField(max_length=200, null=True)
    redirect_uri = models.CharField(max_length=200, null=True)

    def __unicode__(self):
        return self.client_id
