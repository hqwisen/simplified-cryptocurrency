import httplib2
from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import Blockchain
# /relay/blockchain
from relay.apps import RelayConfig
from relay.relay import Relay


class BlockchainView(APIView):

    def get(self, request):
        blockchain = Relay.server().blockchain
        data = Blockchain.serialize(blockchain)
        return Response(data)



class BlockView(APIView):

    def post(self, request):
        h = httplib2.Http()
        resp, content = h.request("http://" + RelayConfig.master_ip + "/master/block",
                                  "POST", body=str(request.data))
        print(resp)
        print(content)
        return Response("Successfully received", status=200)
