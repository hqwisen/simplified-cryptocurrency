from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import Block
from common.serializers import BlockSerializer


class BlockchainView(APIView):
    # serializer_class = BlockSerializer
    # TODO Build a pagination for part of blockchain request
    # pagination_class = None

    def post(self, request):
        print(request.data)
        block = BlockSerializer(request.data)
        # print(block.header)
        return Response("This is correct")

    def get(self, request):
        block = Block(header="hash", nonce=5)
        #serializer = BlockSerializer()
        return Response(data=BlockSerializer(block).serialize(block))
        # return Block.objects.all()

    # def create(self, request, *args, **kwargs):
    #     print(request.data)
    #    serializer = self.get_serializer(data=request.data)
    #    print(serializer.is_valid())
    #    return super(generics.ListCreateAPIView, self).create(request, args, kwargs)
