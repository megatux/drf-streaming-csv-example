from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User


def test_user_list(django_user_model):
    client = APIClient()
    list_url = reverse('user-list')

    user_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
    }
    user = User.objects.create(**user_data)

    response = client.get(list_url)
    assert response.status_code == status.HTTP_200_OK
    assert user_data['username'] in str(response.content)


def test_new_user(django_user_model):
    django_user_model.objects.create(username="someone", password="something")
    assert django_user_model.objects.count() == 1
