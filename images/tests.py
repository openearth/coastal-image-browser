from django.test import TestCase
from images.models import Images, Sites
# Create your tests here.


class ViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.sites = Images.objects.create(location='test.jpg', site='zandmotor', epoch=0, camera=1, image_type='snap', day_minute=0, inarchive=1)


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
