from django.conf.urls import url

from master.views import BlockchainView, BlockView

urlpatterns = [
    url(r'blockchain', BlockchainView.as_view()),
    url(r'block', BlockView.as_view()),
]
