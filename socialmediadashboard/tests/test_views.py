from django.test import TestCase,Client
from rest_framework.test import (APITestCase)
from rest_framework_api_key.models import APIKey

from  django.contrib.auth.models import User
from rest_framework import status
from django.urls import reverse


class SocialDashBoardTest(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create(email="test@test.com")
        self.user.set_password('1234')
        self.user.save()
        self.url = reverse('get-social-media-dashboard' )
        api_key, key = APIKey.objects.create_key(name="my-remote-service")
        self.client.credentials(HTTP_AUTHORIZATION=f"Api-Key {key}")

    def test_for_missing_keyword(self):
        response = self.client.get(path=self.url  + "?network=twitter")
        print(response.json()['status'])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()['status'], False)
        self.assertEqual(response.json()['Message'],  "You Need To Enter At least A Keyword")

    def test_for_added_keyword(self):
        response = self.client.get(path=self.url  + "?keyword=testing&network=twitter")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_social_media_filter_by_network(self):
        response = self.client.get(path=self.url + "?keyword=testing&network=twitter")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_social_media_filter_by_date_range(self):
        response = self.client.get(path=self.url + "?keyword=testing&from_date=2022-10-05&to_date=2022-11-05")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_get_social_media_filter_by_multiple(self):
        response = self.client.get(path=self.url + "?keyword=testing&from_date=2022-10-05&to_date=2022-11-05&language=ar")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_catch_error_on_invalid_filter(self):
        response = self.client.get(path=self.url + "?keyword=testing&from_date=2022-10-05&to_date=2022-11-05&city=greece") # city is the invalid filter here
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)