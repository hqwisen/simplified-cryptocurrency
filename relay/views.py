import logging

from rest_framework import generics

from common.models import Block, Transaction
from common.serializers import BlockSerializer, TransactionSerializer

logger = logging.getLogger(__name__)


class BlockchainView(generics.ListAPIView):
    model_class = Block
    serializer_class = BlockSerializer
    # TODO Build a pagination for part of blockchain request
    pagination_class = None

    def get_queryset(self):
        return Block.objects.all()


class BlockView:
    pass


class TransactionView(generics.ListAPIView):
    model_class = Transaction
    serializer_class = TransactionSerializer
    pagination_class = None

    def get_queryset(self):
            return Transaction.objects.all()
