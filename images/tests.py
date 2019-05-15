from django.test import TestCase
from images.models import Images, Sites
# Create your tests here.


class ViewTests(TestCase):

    def SetUp(self):
        pass

    def test_api_root(self):
        response = self.client.get('/api/')
        self.assertEqual(response.status_code, 200)

    def test_api_sites(self):
        response = self.client.get('/api/sites/')
        self.assertEqual(response.status_code, 200)

    def test_api_images(self):
        response = self.client.get('/api/images/')
        self.assertEqual(response.status_code, 200)

    def test_api_images_mostrecent(self):
        response = self.client.get('/api/images_mostrecent/')
        self.assertEqual(response.status_code, 200)
