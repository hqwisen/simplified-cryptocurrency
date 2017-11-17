from django.conf.urls import url

from relay.views import BlockCollection

urlpatterns = [
    url(r'blocks', BlockCollection.as_view()),
]
