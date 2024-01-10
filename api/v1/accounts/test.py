from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views


class UrlsTest(TestCase):
    def test_token_obtain_pair_url_resolves(self):
        url = reverse('api_v1_accounts:token_obtain_pair')
        self.assertEqual(resolve(url).func.view_class, TokenObtainPairView)
    
    def test_token_refresh_url_resolves(self):
        url = reverse('api_v1_accounts:token_refresh')
        self.assertEqual(resolve(url).func.view_class, TokenRefreshView)

    def test_login_rider_account_url_resolves(self):
        url = '/login-rider/'
        self.assertEqual(resolve(url).func, views.login_rider)

    def test_login_driver_account_url_resolves(self):
        url = '/driver-login/'
        self.assertEqual(resolve(url).func, views.login_driver)
