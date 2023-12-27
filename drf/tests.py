from django.contrib.auth.models import User


def test_new_user(django_user_model):
    django_user_model.objects.create(username="someone", password="something")
    assert django_user_model.objects.count() == 1
