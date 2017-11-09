# encoding: utf-8
from django.shortcuts import render
from form import AuthorizeForm
from django.views.generic import View
from django.utils.decorators import method_decorator
from decorators import validate_request
from django.http import HttpResponse, HttpResponseRedirect
from application.tokens.models import OAuthScope
from application.credentials.models import OAuthUser

from responsetypes import factory
from django.core.urlresolvers import reverse_lazy


class AuthorizeView(View):
    initial = {}
    template_name = 'web/authorize.html'
    form_class = AuthorizeForm

    @method_decorator(validate_request)
    def dispatch(self, *args, **kwargs):
        return super(AuthorizeView, self).dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return self._render(request, form, u"")

    def _render(self, request, form, emg):
        return HttpResponse(render(request, self.template_name, {
            'title': 'Authorize',
            'client': request.client,
            'form': form,
            'scopes': OAuthScope.objects.all(),
            'emg': emg,
        }))

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = OAuthUser.objects.get(email=email)
            except OAuthUser.DoesNotExist:
                emg = u'未找到该用户'
                return self._render(request, form, emg)

            if not user.verify_password(password):
                emg = u'密码不正确'
                return self._render(request, form, emg)

            request.user = user
            return factory(request.response_type).process(
                client=request.client,
                authorize=form.cleaned_data['authorize'],
                scopes=form.cleaned_data['scopes'],
                redirect_uri=request.redirect_uri,
                state=request.state,
                request=request,
            )
        else:
            return self._render(request, form, u"form表单填写不正确")
