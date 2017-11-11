from django.conf.urls import url

from application.tokens.views import *

urlpatterns = [
    url(r'^tokens/?', TokenView.as_view(), name="tokens"),
    url(r'^getuserinfo/?', OAuthUserAccessTokenResponse.as_view(), name='getuserinfo'),

]