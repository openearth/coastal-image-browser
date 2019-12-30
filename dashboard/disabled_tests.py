from django.test import TestCase

from images.models import Images, Sites

# Create your tests here.


class ViewTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.sites = Sites.objects.create(site='zandmotor', country='NL', mincam=1, maxcam=12)


    def SetUp(self):
        pass

    def test_dashboard(self):
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)

    def test_json_heatmap1(self):
        response = self.client.get('/dashboard/json/heatmap/all')
        self.assertEqual(response.status_code, 200)

    def test_json_heatmap2(self):
        response = self.client.get('/dashboard/json/heatmap/all')
        self.assertContains(response, "Acquired images")

    def test_json_heatmap3(self):
        response = self.client.get('/dashboard/json/heatmap/zandmotor')
        self.assertContains(response, "Acquired images at zandmotor")