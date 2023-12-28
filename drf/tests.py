from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from drf.views import UserViewSet


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


def test_user_list_streaming(django_user_model):
    client = APIClient()
    list_url = reverse('user-streaming_view')

    users_data = [
        {
            'username': 'testuser',
            'email': 'testuser@example.com',
        },
        {
            'username': 'testuser2',
            'email': 'testuser2@example.com',
        }
    ]
    user1 = User.objects.create(**users_data[0])
    user2 = User.objects.create(**users_data[1])

    response = client.get(list_url)
    assert response.status_code == status.HTTP_200_OK

    # Read and decode the streamed content
    streamed_content = b"".join(response.streaming_content).decode('utf-8')

    # Assert the content is as expected
    expected_content = users_data[0]['username'] + "," + \
        users_data[0]['email'] + "," + str(user1.is_staff) + "\n"
    assert expected_content in streamed_content

    expected_content = users_data[1]['username'] + "," + \
        users_data[1]['email'] + "," + str(user2.is_staff) + "\n"
    assert expected_content in streamed_content

    # Assert the CSV line count is ok (header line + records)
    assert streamed_content.count("\n") == 1 + (2*UserViewSet.DUP_QUERYSET)


def test_new_user(django_user_model):
    django_user_model.objects.create(username="someone", password="something")
    assert django_user_model.objects.count() == 1
