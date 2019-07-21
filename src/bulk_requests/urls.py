from django.conf.urls import url

from bulk_requests.views import BulkGETView


urlpatterns = [
    url(r'^bulk-get/$', BulkGETView.as_view(), name='bulk-get'),
]
