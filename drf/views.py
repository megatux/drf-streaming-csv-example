from django.http import StreamingHttpResponse
from rest_framework import serializers, viewsets
from django.contrib.auth.models import User
from rest_framework.decorators import action


class QuerysetIterator:
    def __init__(self, queryset, n):
        self.queryset = queryset
        self.n = n
        self.counter = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.counter < self.n:
            self.counter += 1
            return self.queryset.all()
        else:
            raise StopIteration


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    DUP_QUERYSET = 30

    def _item_to_csv(self, item):
        return item.username + "," + item.email + "," + str(item.is_staff) + "\n"

    def stream_data(self, queryset):
        iterator = QuerysetIterator(queryset, self.DUP_QUERYSET)
        for items in iterator:
            for item in items:
                yield str(self._item_to_csv(item))

    @action(methods=["GET"], detail=False, url_path="streaming_view", url_name="streaming_view",)
    def streaming_view(self, request):
        queryset = User.objects.all()

        response = StreamingHttpResponse(
            self.stream_data(queryset), content_type="text/csv")
        return response
