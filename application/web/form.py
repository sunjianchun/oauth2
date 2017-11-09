# coding:utf-8
from django import forms
from application.tokens.models import OAuthScope


class AuthorizeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AuthorizeForm, self).__init__(*args, **kwargs)
        self.fields['email'] = forms.CharField(
            label=u'用户名/邮箱',
            widget=forms.TextInput(attrs={'type': 'email'}),
            required=False,
        )
        self.fields['password'] = forms.CharField(
            label=u'密码',
            widget=forms.TextInput(attrs={'type': 'password'}),
            required=False,
        )
        self.fields['authorize'] = forms.BooleanField()
        self.fields['scopes'] = forms.ModelMultipleChoiceField(
            queryset=OAuthScope.objects.all(),
            widget=forms.CheckboxSelectMultiple,
        )
