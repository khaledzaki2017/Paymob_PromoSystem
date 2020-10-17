from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from core.models import Promo, User
from django.utils import timezone


SAMPLE_ADMIN= {
            'username': 'test_admin',
            'password': 'password'
        }
SAMPLE_USER={
            'username': 'test_user',
            'password': 'password'
        }


class PromoAPITestCase(APITestCase):
    def setUp(self):
        # create admin user
        admin = User(username="test_admin", email="test_admin@test.com", is_staff=True)
        admin.set_password("password")
        admin.save()
        # create user
        user = User(username="test_user", email="test_user@test.com", is_staff=False)
        user.set_password("password")
        user.save()

        # create promo for user
        promo = Promo(
            _type="try",
            promo="tryme",
            amount=2,
            user=user,
            start_at=timezone.now(),
            end_at=timezone.now()
        )
        promo.save()

    def login_and_create_promo(self):
        data = SAMPLE_ADMIN
        url = api_reverse("api-login")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token =response.data.get("token")
        if token is not None:
            _user = User.objects.filter(username='test_user')[0]
            data = {
                "user":_user.pk,
                "_type": "try",
                "promo": "tryme",
                "amount": 2,
                "start_at": timezone.now(),
                "end_at": timezone.now(),
                "is_active": False,
            }
            url = api_reverse('api-promo:promo-controller-list')
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' +token)  
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def login_and_create_promo(self):
        data =SAMPLE_USER
        url = api_reverse("api-login")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token =response.data.get("token")
        if token is not None:
            _user = User.objects.filter(username='test_user')[0]
            data = {
                "user":_user.pk,
                "_type": "try",
                "promo": "tryme",
                "amount": 2,
                "start_at": timezone.now(),
                "end_at": timezone.now(),
                "is_active": False,
            }
            url = api_reverse('api-promo:promo-controller-list')
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' +token)  
            response = self.client.post(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_promos_without_login(self):
        url = api_reverse('api-promo:list-promo')
        response = self.client.get(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_promos_with_admin_login(self):
        data = SAMPLE_ADMIN
        url = api_reverse("api-login")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token =response.data.get("token")
        if token is not None:
            url = api_reverse('api-promo:list-promo')
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' +token)  
            response = self.client.get(url, {}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_promos_with_user_login(self):
        data =SAMPLE_USER
        url = api_reverse("api-login")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token =response.data.get("token")
        if token is not None:
            url = api_reverse('api-promo:list-promo')
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' +token)  
            response = self.client.get(url, {}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_promo_with_user_login(self):
        data = SAMPLE_USER
        url = api_reverse("api-login")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token =response.data.get("token")
        if token is not None:
            url = api_reverse('api-promo:promo-controller-detail', kwargs={'pk': 1})
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' +token)  
            response = self.client.delete(url, {}, format='json')
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)