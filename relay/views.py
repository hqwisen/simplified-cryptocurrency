from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import Block


class BlockchainView(APIView):

    def get(self, request):
        return Response("From GET")

    def post(self, request):
        block = Block.parse(request.data)
        data = Block.serialize(block)
        return Response({"title": "Hello this is a response from POST", "data": data})
