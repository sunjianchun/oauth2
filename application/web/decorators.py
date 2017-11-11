from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from application.tokens.models import OAuthScope
from application.credentials.models import OAuthClient
from django.conf import settings


def validate_request(view):
    def _err_response(request, error, error_description):
        return HttpResponse(render(request, 'web/error.html', {
            'title': 'Error',
            'error': error,
            'error_description': error_description,
        }))

    def _wrapper(request, *args, **kwargs):
        client_id = request.POST.get('client_id', None)
        if not client_id:
            client_id = request.GET.get('client_id', None)
            if not client_id:
                return _err_response(request, u'invalid_client', u'No client id supplied')
        try:
            request.client = OAuthClient.objects.get(client_id=client_id)
        except OAuthClient.DoesNotExist:
            return _err_response(request, u'invalid_client', u'The client id supplied is invalid')

        response_type = request.POST.get('response_type', None)
        if not response_type:
            response_type = request.GET.get('response_type', None)
            if not response_type:
                return _err_response(request, u'invalid_response_type', u'No response_type id supplied')

        request.response_type = response_type

        redirect_uri = request.POST.get('redirect_uri', None)
        if not redirect_uri:
            redirect_uri = request.GET.get('redirect_uri', None)
            if not redirect_uri:
                return _err_response(request, u'invalid_uri', u'No redirect URI was supplied or stored')

        request.redirect_uri = redirect_uri

        state = request.POST.get('state', None)
        if not state:
            state = request.GET.get('state', None)
            if not state:
                return _err_response(request, u'invalid_request', u'The state parameter is required')

        request.state = state

        if request.method == "POST":
            scopes = request.POST.getlist('scopes', None)
            request.scopes = OAuthScope.objects.filter(pk__in=scopes)

        else:
            scopes = request.GET.get('scopes', None)
            if not scopes:
                scopes = []
            else:
                scopes = scopes.strip().split(',')
                scopes = OAuthScope.objects.filter(scope__in=scopes)
            if settings.APPEND_DEFAULT_SCOPES:
                default_scopes = OAuthScope.objects.filter(is_default=True)
                request.scopes = list(set(default_scopes) | set(scopes))
            else:
                request.scopes = scopes

        try:
            request.client = OAuthClient.objects.get(client_id=client_id)
        except OAuthClient.DoesNotExist:
            return _err_response(request, u'invalid_client', u'The client id supplied is invalid')

        return view(request, *args, **kwargs)

    return _wrapper
