from django.urls import path

from . import apis

urlpatterns=[
    path("register/", apis.RegisterApi.as_view(), name="register"),
    path("login/", apis.LoginApi.as_view(), name="login" ),
    path("me/", apis.UserAPI.as_view(), name="me"),
    path("logout/", apis.LogoutAPI.as_view(), name="logout")
]


