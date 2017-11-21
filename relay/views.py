import logging

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import Block, Transaction
from common.serializers import BlockSerializer, TransactionSerializer

logger = logging.getLogger(__name__)




class TransactionView(APIView):

    def post(self, request):
        # transaction = TransactionSerializer(request.data)
        return Response("Transaction POST")


    def get(self, request):
        # transaction = TransactionSerializer(request.data)
        return "Transaction GET"

            #Relay.server.add_transaction(transaction)

class RelayView(APIView):

    def get(self, request):
        return Response("Hello from GET")

    def post(self, request):
        return Response("Hello from POST")

# class TransactionView(generics.ListAPIView):
 #   model_class = Transaction
  #  serializer_class = TransactionSerializer
   # pagination_class = None

    #def get_queryset(self):
#       return Transaction.objects.all()
