from django.conf.urls import url

from application.tokens.views import TokenView

urlpatterns = [
    url(r'^tokens/?', TokenView.as_view(), name="tokens"),
]