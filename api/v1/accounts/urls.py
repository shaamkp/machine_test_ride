from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from django.urls import path, re_path

from . import views

app_name = "api_v1_accounts"

urlpatterns = [
    re_path(r'^login-rider/$', views.login_rider, name="login-rider"),
    re_path(r'^driver-login/$', views.login_driver, name="login-driver"),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]