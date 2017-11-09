from __future__ import unicode_literals
from django.utils import timezone
from django.db import models
from django.conf import settings
from application.credentials.models import OAuthUser, OAuthClient


class ExpireMixin(models.Model):
    expire_at = models.DateTimeField()

    class Meta:
        abstract = True

    def check_expire(self):
#        return timezone.now() > self.expire_at
        return False
    @property
    def expire_in(self):
        now = timezone.now()
        if now >= self.expire_at:
            return 0
        else:
            return int(round((self.expire_at - now).total_seconds()))

    @classmethod
    def next_expire(cls):
        try:
            lifetime = settings.OAUTH2_SERVER[cls.lifetime_setting]
        except KeyError:
            lifetime = cls.default_lifetime
        return timezone.now() + timezone.timedelta(seconds=lifetime)


class OAuthScope(models.Model):
    scope = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    is_default = models.BooleanField(default=False)

    def __unicode__(self):
        return self.scope


class TokenCodeMixin(models.Model):
    scopes = models.ManyToManyField(OAuthScope)
    client = models.ForeignKey(OAuthClient)
    user = models.ForeignKey(OAuthUser, null=True)

    @property
    def scope(self):
        return " ".join([s.scope for s in self.scopes.all()])

    class Meta:
        abstract = True

    lifetime_setting = 'REFRESH_TOKEN_LIFETIME'
    default_lifetime = 1209600  # 14 days


class OAuthRefreshToken(ExpireMixin):
    refresh_token = models.CharField(max_length=40, unique=True)

    def __unicode__(self):
        return self.refresh_token

    lifetime_setting = 'REFRESH_TOKEN_LIFETIME'
    default_lifetime = 1209600  # 14 days


class OAuthAccessToken(TokenCodeMixin, ExpireMixin):
    refresh_token = models.OneToOneField(OAuthRefreshToken, related_name="access_token", null=True)
    access_token = models.CharField(max_length=40, unique=True)

    @property
    def token_type(self):
        return 'Bearer'

    def __unicode__(self):
        return self.access_token

    lifetime_setting = 'ACCESS_TOKEN_LIFETIME'
    default_lifetime = 3600


class OAuthAuthorizationCode(TokenCodeMixin, ExpireMixin):
    code = models.CharField(max_length=40, unique=True)
    redirect_uri = models.CharField(max_length=200, null=True)

    def __unicode__(self):
        return self.code

    lifetime_setting = 'AUTH_CODE_LIFETIME'
    default_lifetime = 3600
