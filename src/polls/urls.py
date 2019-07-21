from django.conf.urls import url

from polls.views import PollListView


urlpatterns = [
    url(r'^polls/$', PollListView.as_view(), name='poll-list'),
]
