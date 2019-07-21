from django.conf.urls import url

from bulk_requests.tests.mocks.views import SomeAPI, AnotherAPI
from bulk_requests.views import BulkGETView


urlpatterns = [
    url(r'^bulk-get/$', BulkGETView.as_view(), name='bulk-get'),
    url(r'^some-api/$', SomeAPI.as_view(), name='some-api'),
    url(r'^another-api/$', AnotherAPI.as_view(), name='another-api'),
]
