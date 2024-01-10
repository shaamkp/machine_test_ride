from django.test import TestCase
from django.urls import resolve
from . import views


class UrlsTest(TestCase):
    def test_request_ride_url_resolves(self):
        url = '/request-ride/'
        self.assertEqual(resolve(url).func, views.create_ride)

    def test_list_rides_url_resolves(self):
        url = '/list-rides/'
        self.assertEqual(resolve(url).func, views.list_rides)

    def test_list_ride_url_resolves(self):
        url = '/list-ride/(?P<pk>\d+)/'
        self.assertEqual(resolve(url).func, views.list_ride)

    def test_update_ride_location_url_resolves(self):
        url = '/update-ride-location/(?P<pk>\d+)/'
        self.assertEqual(resolve(url).func, views.list_ride)

    def test_track_ride_location_url_resolves(self):
        url = '/track-ride-location/(?P<pk>\d+)/'
        self.assertEqual(resolve(url).func, views.track_ride_location)

    def test_ride_confirmation_url_resolves(self):
        url = '/ride-confirmation/'
        self.assertEqual(resolve(url).func, views.ride_confirmation)
