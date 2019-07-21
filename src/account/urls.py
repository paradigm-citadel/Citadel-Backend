from django.conf.urls import url

from rest_framework import routers
from rest_framework.authtoken import views

from account.views.account import AccountViewSet
from account.views.auth import RegisterView, RestorePasswordView


router = routers.SimpleRouter()
urlpatterns = [
    url('^account/$', AccountViewSet.as_view(
        {'get': 'retrieve', 'put': 'update'}
    )),
    url('^account/change-password/$', AccountViewSet.as_view(
        {'put': 'change_password'}
    )),
    url('^register/$', RegisterView.as_view()),
    url('^restore/$', RestorePasswordView.as_view()),
    url('^auth/$', views.obtain_auth_token)
]
