from rest_framework.response import Response
from rest_framework.views import APIView

from relay.relay import Block


class BlockchainView(APIView):

    def get(self, request):
        return Response("From GET")

    def post(self, request):
        print(request.data)
        print(request.data.__class__)
        block = Block.parse(request.data)
        print(block.transactions)
        data = Block.serialize(block)
        # print(serializer.is_valid())
        return Response({"title": "Hello this is a response from POST", "data": data})