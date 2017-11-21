from rest_framework.response import Response
from rest_framework.views import APIView

from relay.models import Block
from relay.serializers import BlockSerializer


class BlockchainView(APIView):

    def get(self, request):
        block = Block.create("THIS IS A HEADER", 100)
        return Response(BlockSerializer(block).data)

    def post(self, request):
        return Response("Hello this is a response from POST")