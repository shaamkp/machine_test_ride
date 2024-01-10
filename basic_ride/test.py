import unittest
from django.urls import resolve
from django.test import SimpleTestCase
from django.contrib import admin

from api.v1.accounts.urls import views

class TestUrls(SimpleTestCase):

    def test_admin_url_resolves(self):
        """
        Test if the admin URL resolves to the correct view
        """
        url = '/'
        resolver = resolve(url)
        self.assertEqual(resolver.func, admin.site.urls)

    def test_accounts_api_url_resolves(self):
        """
        Test if the accounts API URL resolves to the correct view
        """
        url = '/api/v1/accounts/'
        resolver = resolve(url)
        self.assertEqual(resolver.func, views.api_v1_accounts)


if __name__ == '__main__':
    unittest.main()
