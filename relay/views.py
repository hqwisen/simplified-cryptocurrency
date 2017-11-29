import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common import client
from common.models import Block, Transaction, ParseException, Blockchain
from common.views import BlockchainGETView
from relay.relay import Relay, RelayError

from django.conf import settings

logger = logging.getLogger(__name__)


class BlockchainView(BlockchainGETView):

    def post(self, request):
        try:
            block = Block.parse(request.data)
            updated = self.server.update_blockchain(block)
            # if not updated:
            #     last_index = self.server.blockchain_size() - 1
            #     response = client.get(settings.MASTER_IP,
            #                           'blockchain?start=%d&end=%d' % (last_index, -1))
            #     blockchain = Blockchain.parse(response.data)
            #     self.server.add_blocks(blockchain.blocks)
            return Response(status=status.HTTP_201_CREATED)
        except ParseException as e:
            return Response(str(e), status=status.HTTP_406_NOT_ACCEPTABLE)

    @property
    def server(self):
        return Relay()


class BlockView(APIView):
    def post(self, request):
        response = client.post(settings.MASTER_IP, 'blockchain', request.data)
        # TODO should we send an anwser base on master node response ?
        return Response("Successfully received", status=status.HTTP_200_OK)


class TransactionView(APIView):
    def get(self, request):
        server = Relay()
        exclude = request.data['exclude_hash'] if 'exclude_hash' in request.data else []
        if 'exclude_hash' not in request.data:
            logger.info("'exclude_hash' not in request")
        transaction = server.get_transaction(exclude)
        if transaction != None:
            return Response(Transaction.serialize(transaction),
                            status=status.HTTP_200_OK)
        else:
            return Response({'errors': 'no transaction to send'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        server = Relay()
        try:
            transaction = Transaction.parse(request.data)
            server.add_transaction(transaction)
            return Response(status=status.HTTP_201_CREATED)
        except (RelayError, ParseException) as e:
            return Response(str(e), status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request):
        server = Relay()
        for transaction in request.data['bad_transactions']:
            server.remove_transaction(transaction)
