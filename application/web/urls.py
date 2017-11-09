from django.conf.urls import url
from application.web.views import AuthorizeView

urlpatterns = [
    url(r'^authorize/?', AuthorizeView.as_view(), name='authorize'),
]
