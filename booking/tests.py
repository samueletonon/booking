import datetime

from django.test import TestCase
from django.utils import timezone
from django.test import Client

from .models import *


class CheckBooking(TestCase):
    def test_failed_login(self):
        client = Client()
        response = client.post(
            "/accounts/login/", {"username": "samu", "password": "samu2"}
        )
        self.assertEqual(response.status_code, 200)

    def login(self):
        client = Client()
        response = client.post(
            "/accounts/login/?next=/", {"username": "samu", "password": "samu"}
        )
        return(client)

    def test_booking(self):
        client  = self.login()
        response = client.post("/pubsub",{"day": "20021211"})
        self.assertEqual(response.status_code, 302)
