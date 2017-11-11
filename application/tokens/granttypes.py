import uuid
from django.conf import settings
from application.tokens.models import *
from oauth2.exceptions import *


def factory(request):
    if request.grant_type == settings.AUTHORIZATION_CODE:
        return AuthorizationGrantTypeAccessToken(request)
    elif request.grant_type == settings.PASSWORD:
        return PasswordGrantTypeAccessToken(request)
    elif request.grant_type == settings.CLIENT:
        return CredentialsGrantTypeAccessToken(request)
    elif request.grant_type == settings.REFRESH:
        return RefreshTokenGrantTypeAccessToken(request)


class CreateTokenMixin(object):
    def create_assess_token(self):
        refresh_token = OAuthRefreshToken.objects.create(
            refresh_token=uuid.uuid4(),
            expire_at=OAuthRefreshToken.next_expire()
        )
        access_token = OAuthAccessToken.objects.create(
            refresh_token=refresh_token,
            access_token=uuid.uuid4(),
            expire_at=OAuthAccessToken.next_expire(),
            user=self.user,
            client=self.client,
        )

        access_token.scopes.add(*self.scopes)
        return access_token


class AuthorizationGrantTypeAccessToken(CreateTokenMixin):
    def __init__(self, request):
        self.scopes = request.auth_code.scopes.all()
        self.user = request.auth_code.user

        print type(request.client)
        self.client = request.client
        print type(self.client)
        self.auth_code = request.auth_code
        if self.auth_code.check_expire():
            self.auth_code.delete()
            raise ExpiredAuthorizationCodeException()

    def grant(self):
        access_token = self.create_assess_token()
        self.auth_code.delete()
        return access_token


class PasswordGrantTypeAccessToken(CreateTokenMixin):
    def __init__(self, request):
        self.user = request.user
        self.client = request.client
        self.scopes = request.scopes

    def grant(self):
        return self.create_assess_token()


class CredentialsGrantTypeAccessToken(CreateTokenMixin):
    def __init__(self, request):
        self.user = None
        self.client = request.client
        self.scopes = request.scopes

    def grant(self):
        return self.create_assess_token()


class RefreshTokenGrantTypeAccessToken(CreateTokenMixin):
    def __init__(self, request):
        self.refresh_token = request.refresh_token

        self.user = self.refresh_token.access_token.user
        self.client = self.refresh_token.access_token.client
        self.access_token = self.refresh_token.access_token
        self.scopes = request.scopes

        if self.refresh_token.check_expire():
            self.refresh_token.delete()
            self.access_token.delete()
            raise ExpiredRefreshTokenException()

    def grant(self):
        access_token = self.create_assess_token()
        self.refresh_token.access_token.delete()
        self.refresh_token.delete()
        return access_token
