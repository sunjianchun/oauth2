from rest_framework import serializers

from application.tokens.models import OAuthAccessToken
from application.credentials.models import OAuthUser

class OAuthAccessTokenSerializer(serializers.ModelSerializer):
    refresh_token = serializers.CharField(
        source='refresh_token.refresh_token'
    )

    class Meta:
        model = OAuthAccessToken
        fields = ('id', 'access_token', 'expire_in', 'token_type', 'scope', 'refresh_token')
