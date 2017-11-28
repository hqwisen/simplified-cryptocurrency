import httplib2
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from common.models import Blockchain, Block, Transaction, ParseException
from relay.apps import RelayConfig
from relay.relay import Relay, RelayError

from common.views import BlockchainGetView

import logging

logger = logging.getLogger(__name__)

class BlockchainView(BlockchainGetView):

    def post(self, request):
        server = self.get_server()
        try:
            block = Block.parse(request.data)
            updated = server.update_blockchain(block)
            if not updated:
                request full blockchain
            return Response(status=status.HTTP_201_CREATED)
        except ParseException as e:
            return Response(str(e), status=status.HTTP_406_NOT_ACCEPTABLE)

    def get_server(self):
        return Relay()


class BlockView(APIView):

    def post(self, request):
        h = httplib2.Http()
        resp, content = h.request("http://" + RelayConfig.master_ip + "/master/block",
                                  "POST", body=str(request.data))
        # TODO The miner should also send his address, to be forwarded to the master for the reward
        return Response("Successfully received", status=status.HTTP_201_CREATED)


class TransactionView(APIView):

    def get(self, request):
        server = Relay()
        exclude =  request.data['exclude_hash'] if 'exclude_hash' in request.data else []
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

