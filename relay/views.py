import httplib2
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import Blockchain, Block
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
        return Response(status=201)


class BlockView(APIView):

    def post(self, request):
        h = httplib2.Http()
        resp, content = h.request("http://" + RelayConfig.master_ip + "/master/block",
                                  "POST", body=str(request.data))
        print(resp)
        print(content)
        return Response("Successfully received", status=200)
