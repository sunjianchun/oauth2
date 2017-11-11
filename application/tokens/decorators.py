import base64
from functools import wraps
from django.conf import settings

from django.utils.decorators import available_attrs
from oauth2.exceptions import *
from application.tokens.models import *
from application.credentials.models import *


def _check_access_token_in_header(request):
    if not 'HTTP_AUTHORIZATION' in request.META:
        return False
    auth_method, auth = request.META['HTTP_AUTHORIZATION'].split(' ')
    if auth_method.lower() != 'bearer':
        return False

    return auth


def _check_access_token_in_post(request):
    if 'access_token' not in request.POST:
        return False

    return request.POST['access_token']


def _check_access_token_in_get(request):
    if 'access_token' not in request.GET:
        return False

    return request.GET['access_token']


def authentication_required(func):
    '''
        curl -H "Authorization: Bearer <ACCESS_TOKEN>" http://www.example.com
    :return:
    '''

    @wraps(func, assigned=available_attrs(func))
    def _inner(request, *args, **kwargs):
        access_token = _check_access_token_in_header(request)
        if not access_token:
            access_token = _check_access_token_in_post(request)
            if not access_token:
                access_token = _check_access_token_in_get(request)
                if not access_token:
                    raise AccessTokenRequiredException()

        try:
            access_token = OAuthAccessToken.objects.get(access_token=access_token)
        except OAuthAccessToken.DoesNotExist:
            raise InvalidAccessTokenException()

        if access_token.check_expire():
            raise ExpiredAccessTokenException()

        request.access_token = access_token
        return func(request, *args, **kwargs)

    return _inner




def validate_request(func):
    '''

    :param func:
    :return:
    '''

    def _validate_grant_type(request):

        grant_type = request.POST.get('grant_type', None)

        if not grant_type:
            raise GrantTypeRequiredException()
        if grant_type not in settings.VALID_GRANT_TYPES:
            raise InvalidGrantTypeException()

        if grant_type == settings.AUTHORIZATION_CODE:
            code = request.POST.get('code', None)
            if not code:
                code = request.GET.get('code', None)
                if not code:
                    raise CodeRequiredException()

            try:
                request.auth_code = OAuthAuthorizationCode.objects.get(code=code)
            except OAuthAuthorizationCode.DoesNotExist:
                raise AuthorizationCodeNotFoundException()

            request.scopes = request.auth_code.scopes.all()

        if grant_type == settings.PASSWORD:
            username = request.POST.get('username', None)
            if not username:
                username = request.GET.get('username', None)
                if not username:
                    raise UsernameRequiredException()

            password = request.POST.get('password', None)
            if not password:
                password = request.GET.get('password', None)
                if not password:
                    raise PasswordRequiredException()

            try:
                user = OAuthUser.objects.get(email=username)
            except OAuthUser.DoesNotExist:
                raise InvalidUserCredentialsException()

            if not user.verify_password(password):
                raise InvalidUserCredentialsException()

            request.user = user

            scopes = request.POST.get('scopes', None)
            if not scopes:
                scopes = request.GET.get('scopes', None)
            if not scopes:
                scopes = []
            else:
                scopes = scopes.strip().split(',')
                scopes = OAuthScope.objects.filter(scope__in=scopes)
                if settings.APPEND_DEFAULT_SCOPES:
                    default_scopes = OAuthScope.objects.filter(is_default=True)
                    request.scopes = list(set(scopes) | set(default_scopes))
                else:
                    request.scopes = scopes

        if grant_type == settings.REFRESH:
            refresh_token = request.POST.get('refresh_token', None)
            if not refresh_token:
                refresh_token = request.GET.get('refresh_token', None)
                if not refresh_token:
                    raise RefreshTokenRequiredException()

            try:
                request.refresh_token = OAuthRefreshToken.objects.get(refresh_token=refresh_token)
            except OAuthRefreshToken.DoesNotExist:
                raise RefreshTokenNotFoundException()

            scopes = request.POST.get('scopes', None)
            if not scopes:
                scopes = request.GET.get('scopes', None)
            if not scopes:
                request.scopes = request.refresh_token.access_token.scopes.all()

            scopes = scopes.strip().split(',')
            scopes = OAuthScope.objects.filter(scope__in=scopes)

            request.scopes = list(set(scopes) & set(request.refresh_token.access_token.scopes.all()))

        request.grant_type = grant_type

    def _extract_client(request):
        client_id, client_secret = None, None

        if 'HTTP_AUTHORIZATION' in request.META:
            auth_method, auth = request.META['HTTP_AUTHORIZATION'].split(': ')
            if auth_method.lower() == 'basic':
                client_id, client_secret = base64.b64decode(auth).split(':')

        if not client_id or not client_secret:
            client_id = request.POST.get('client_id', None)
            client_secret = request.POST.get('client_secret', None)
            if not client_id or not client_secret:
                client_id = request.GET.get('client_id', None)
                client_secret = request.GET.get('client_secret', None)
                if not client_id or not client_secret:
                    raise ClientCredentialsRequiredException()

        try:
            client = OAuthClient.objects.get(client_id=client_id)
        except OAuthClient.DoesNotExist:
            raise InvalidClientCredentialsException()

        if not client.verify_password(client_secret):
            raise InvalidClientCredentialsException()

        request.client = client

    def _extract_scope(request):
        if settings.OAUTH2_SERVER['IGNORE_CLIENT_REQUESTED_SCOPE']:
            request.scopes = OAuthScope.objects.filter(is_default=True)
            return

        if hasattr(request, "scopes"):
            if len(request.scopes) == 0:
                request.scopes = OAuthScope.objects.filter(is_default=True)
        else:
            request.scopes = OAuthScope.objects.filter(is_default=True)

    def decorator(request, *args, **kwargs):
        _validate_grant_type(request)
        _extract_client(request)
        _extract_scope(request)

        return func(request, *args, **kwargs)

    return decorator
