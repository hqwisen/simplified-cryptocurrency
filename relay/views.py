import httplib2
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status as httpstatus

from common.models import Blockchain, Block, Transaction
from relay.apps import RelayConfig
from relay.relay import Relay


class BlockchainView(APIView):

    def get(self, request):
        blockchain = Relay.blockchain
        try:
            start, end = int(request.query_params['start']), int(request.query_params['end'])
            blockchain = Relay.part_of(start, end)
        except KeyError as e:
            print("Error while parsing params: %s" % e)
        data = Blockchain.serialize(blockchain)
        return Response(data)

    def post(self, request):
        data = request.data
        block = Block.parse(data)
        Relay.blockchain.add_block(block)
        # TODO remove transaction that are in new block
        return Response(status=201)


class BlockView(APIView):

    def post(self, request):
        h = httplib2.Http()
        resp, content = h.request("http://" + RelayConfig.master_ip + "/master/block",
                                  "POST", body=str(request.data))
        print(resp)
        print(content)
        return Response("Successfully received", status=200)


class TransactionView(APIView):

    def get(self, request):
        exclude = request.data['exclude_txid']
        transaction = Relay.get_transaction(exclude)
        if transaction != None:
            data = Transaction.serialize(transaction)
            status = httpstatus.HTTP_200_OK
        else:
            data = None
            status = httpstatus.HTTP_404_NOT_FOUND
        return Response(data, status=status)

    def post(self, request):
        transaction = Transaction.parse(request.data)
        # TODO verifier transaction
        Relay.add_transaction(transaction)
        return Response(status=httpstatus.HTTP_201_CREATED)