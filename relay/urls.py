from django.conf.urls import url

from relay.views import BlockchainView

urlpatterns = [
    # url(r'', RelayView.as_view()),
    url(r'blockchain', BlockchainView.as_view()),
    # url(r'block', BlockView.as_view()),
    # url(r'transactions', TransactionView.as_view()),
]
