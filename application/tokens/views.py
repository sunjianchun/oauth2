from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator

from application.tokens.decorators import validate_request
from application.tokens.granttypes import factory

from application.tokens.serializers import OAuthAccessTokenSerializer

class TokenView(APIView):
    @method_decorator(validate_request)
    def post(self, request, *args, **kwargs):
        access_token = factory(request).grant()
        return Response(
            OAuthAccessTokenSerializer(access_token).data,
            status=status.HTTP_201_CREATED,
        )
