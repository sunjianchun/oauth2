from django.contrib import admin
from application.tokens.models import *

class OAuthScopeAdmin(admin.ModelAdmin):
    list_display = ('id', 'scope', 'is_default',)
    search_field = ('scope',)


class OAuthAccessTokenAdmin(admin.ModelAdmin):
    list_display = ('client', 'user', 'access_token', 'refresh_token', 'expire_at')
    search_field = ('access_token', 'client',)


class OAuthRefreshTokenAdmin(admin.ModelAdmin):
    list_display = ('refresh_token', 'expire_at',)
    search_field = ('refresh_token',)


class OAuthAuthorizationCodeAdmin(admin.ModelAdmin):
    list_display = ('client', 'user', 'code', 'redirect_uri',  'expire_at',)
    search_field = ('redirect_uri', 'code',)


admin.site.register(OAuthScope, OAuthScopeAdmin)
admin.site.register(OAuthAccessToken, OAuthAccessTokenAdmin)
admin.site.register(OAuthRefreshToken, OAuthRefreshTokenAdmin)
admin.site.register(OAuthAuthorizationCode, OAuthAuthorizationCodeAdmin)