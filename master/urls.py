from django.conf.urls import url

from master.views import BlockchainView

urlpatterns = [
    url(r'blockchain', BlockchainView.as_view()),
]
