"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
import urllib

from django.http import HttpRequest
from django.test import TestCase
from django.test.client import Client

import HvZ.views
import HvZ.models

UNAME = "rzed@hmc.edu"
PW = "asdf"

class ConfirmEatingWorks(TestCase):
     fixtures = ['eat_test.json']

     anonymous = HvZ.views.anonymous_info()

     def test_Simple_Eating_Case(self):
         fc = "EATEN"

         c = self.client
         c.login(username=UNAME, password=PW)

         c.get('/player/eat')
         response = c.post('/player/eat/',
                           {"feed_code": fc,
                            "meal_day":  1,
                            "meal_hour": 12,
                            "meal_mins": 20,
                            "meal_ap": 1,
                            "description": "Not long for this world..."
                            })

         self.assertEqual(response.status_code, 200)
         self.assertEqual(response.context['preform'], ["You have eaten Poor Sod!"])

def django_to_twilio(number):
     """At least, this is how I assume twilio wants US phone numbers."""
     return "+1" + number.replace("-", "")

class ConfirmTextingWorks(TestCase):
     fixtures = ['eat_test.json']

     def test_texting(self):
          c = self.client

          p = HvZ.models.Player.objects.get(user__username=UNAME)

          response = c.get('/twilio/sms/',
                           {"To": "+19095254551",
                            "From": django_to_twilio(p.cell)
                            })

          self.assertEqual(response.status_code, 200)
          self.assertEqual(response.context['response'],
                           "Valid commands are status, mod, mission, feed, stop, and help.")

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

