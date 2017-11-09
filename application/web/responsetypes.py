import urllib
import uuid
import datetime
from application.tokens.models import OAuthAuthorizationCode, OAuthAccessToken

from django.http import HttpResponseRedirect


def factory(response_type):
    return {
        'code': CodeResponseType(),
        'token': ImplicitResponseType(),
    }[response_type]


class AbstractResponse(object):
    def denied(self, state, redirect_uri):
        query_string = urllib.urlencode({
            'error': u'accessed_denied',
            'error_description': u'The user denied you access to your application.',
            'state': state,
        })

        return HttpResponseRedirect('{}?{}'.format(redirect_uri, query_string))


class CodeResponseType(AbstractResponse):
    def process(self, request, authorize, state, redirect_uri, client, scopes):
        if not authorize:
            return self.denied(state, redirect_uri)

        code = OAuthAuthorizationCode.objects.filter(client=client, user=request.user, redirect_uri=redirect_uri,
                                                     expire_at__gt=datetime.datetime.now())
        if code.count() > 0:
            code.delete()
        auth_code = OAuthAuthorizationCode.objects.create(
            code=uuid.uuid4(),
            redirect_uri=redirect_uri,
            client=client,
            user=request.user,
            expire_at=OAuthAuthorizationCode.next_expire(),
        )
        auth_code.scopes.add(*scopes)

        query_string = urllib.urlencode({
            'code': auth_code.code,
            'state': state,
        })
        return HttpResponseRedirect('{}?{}'.format(redirect_uri, query_string))


class ImplicitResponseType(AbstractResponse):
    def process(self, request, authorize, client, scopes, state, redirect_uri):
        if not authorize:
            return self.denied()
        access_token = OAuthAccessToken.objects.create(
            expire_at=OAuthAccessToken.next_expire(),
            client=client,
            access_token=uuid.uuid4(),
            user=request.user,
        )

        access_token.scopes.add(*scopes)

        query_string = urllib.urlencode({
            'access_token': access_token.access_token,
            'expires_in': access_token.expire_at,
            'token_type': 'token',
            'state': state,
        })
        return HttpResponseRedirect('{}?{}'.format(redirect_uri, query_string))
