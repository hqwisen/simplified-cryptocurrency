from django.conf.urls import url

from relay.views import BlockCollection

urlpatterns = [
    url(r'blockchain', BlockCollection.as_view()),
    url(r'block', BlockCollection.as_view()),
    url(r'transactions', BlockCollection.as_view()),
]
