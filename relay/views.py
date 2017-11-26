import httplib2
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status as httpstatus

from common.models import Blockchain, Block, Transaction, ParseException
from relay.apps import RelayConfig
from relay.relay import Relay, RelayError

from common.views import BlockchainGetView

import logging

logger = logging.getLogger(__name__)


class BlockchainView(BlockchainGetView):
    pass


class BlockView(APIView):

    def post(self, request):
        h = httplib2.Http()
        resp, content = h.request("http://" + RelayConfig.master_ip + "/master/block",
                                  "POST", body=str(request.data))
        # TODO The miner should also send his address, to be forwarded to the master for the reward
        return Response("Successfully received", status=httpstatus.HTTP_201_CREATED)


class TransactionView(APIView):

    def get(self, request):
        exclude =  request.data['exclude_txid'] if 'exclude_txid' in request.data else []
        if 'exclude_txid' not in request.data:
            logger.info("'exclude_txid' not in request")
        transaction = Relay.get_transaction(exclude)
        if transaction != None:
            data = Transaction.serialize(transaction)
            status = httpstatus.HTTP_200_OK
        else:
            data = {'errors': 'no transaction to send'}
            status = httpstatus.HTTP_404_NOT_FOUND
        return Response(data, status=status)

    def post(self, request):
        try:
            transaction = Transaction.parse(request.data)
            Relay.add_transaction(transaction)
            return Response(status=httpstatus.HTTP_201_CREATED)
        except (RelayError, ParseException) as e:
            return Response(str(e), status=httpstatus.HTTP_406_NOT_ACCEPTABLE)

