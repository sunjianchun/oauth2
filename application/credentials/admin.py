from django.contrib import admin
from application.credentials.models import *

class OAuthClientAdmin(admin.ModelAdmin):
    list_display = ('id', 'client_id', 'redirect_uri',)
    search_field = ('client_id',)


class OAuthUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'idCard')
    search_field = ('email',)


admin.site.register(OAuthClient, OAuthClientAdmin)
admin.site.register(OAuthUser, OAuthUserAdmin)