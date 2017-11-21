import logging

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import Block, Transaction
from common.serializers import BlockSerializer, TransactionSerializer

logger = logging.getLogger(__name__)


class BlockchainView(generics.ListCreateAPIView):
    serializer_class = BlockSerializer
    # TODO Build a pagination for part of blockchain request
    pagination_class = None

    def get_queryset(self):
        return Block.objects.all()

    # def create(self, request, *args, **kwargs):
    #     print(request.data)
    #    serializer = self.get_serializer(data=request.data)
    #    print(serializer.is_valid())
    #    return super(generics.ListCreateAPIView, self).create(request, args, kwargs)



class RelayView(APIView):

    def get(self, request):
        return Response("Hello from GET")

    def post(self, request):
        return Response("Hello from POST")

class TransactionView(generics.ListAPIView):
    model_class = Transaction
    serializer_class = TransactionSerializer
    pagination_class = None

    def get_queryset(self):
            return Transaction.objects.all()
