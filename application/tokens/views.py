#encoding: utf-8

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict

from application.tokens.decorators import validate_request, authentication_required
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


class OAuthUserAccessTokenResponse(APIView):
    @method_decorator(authentication_required)
    def get(self, request, *args, **kwargs):
        context = {}

        access_token = request.access_token
        if not access_token.user:
            context["message"] = "Grant type is client_credentials, Auth Server can customer... "
            return Response(context, status.HTTP_200_OK,)
        scopes = request.access_token.scopes.all()
        for scope in scopes:
            user_keys = scope.scope.strip().split('/')
            for key in user_keys:
                context[key.strip()] = model_to_dict(access_token.user)[key.strip()]

        new_context = {}
        for k, v in context.items():
            if k not in new_context:
                new_context[k] = v
        return Response(new_context, status.HTTP_200_OK)
