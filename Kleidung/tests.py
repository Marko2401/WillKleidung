from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import Listing, Category


class SimpleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='tester', password='pass')
        self.cat = Category.objects.create(name='Test', gender='U')
        self.listing = Listing.objects.create(
            seller=self.user,
            title='Test Item',
            description='Just a test',
            category=self.cat,
            price=9.99,
            location='Testville'
        )

    def test_listing_str(self):
        self.assertIn('Test Item', str(self.listing))


class APITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='apiuser', password='apipass')
        self.cat = Category.objects.create(name='API Cat', gender='U')

    def test_listings_list_unauthenticated(self):
        resp = self.client.get('/api/listings/')
        self.assertEqual(resp.status_code, 200)

    def test_create_listing_requires_auth(self):
        data = {
            'title': 'API Item',
            'description': 'desc',
            'category': self.cat.id,
            'price': '5.00',
            'location': 'Test',
        }
        resp = self.client.post('/api/listings/', data)
        self.assertEqual(resp.status_code, 401)

    def test_jwt_auth_and_create(self):
        # obtain token
        token_resp = self.client.post('/api/token/', {'username': 'apiuser', 'password': 'apipass'}, format='json')
        self.assertEqual(token_resp.status_code, 200)
        access = token_resp.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        data = {
            'title': 'API Item',
            'description': 'desc',
            'category': self.cat.id,
            'price': '5.00',
            'location': 'Test',
        }
        resp = self.client.post('/api/listings/', data)
        self.assertEqual(resp.status_code, 201)

