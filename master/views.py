from django.shortcuts import render

from rest_framework import generics

from common.models import Block
from common.serializers import BlockSerializer


class BlockchainView(generics.ListCreateAPIView):
    model_class = Block
    serializer_class = BlockSerializer
    # TODO Build a pagination for part of blockchain request
    pagination_class = None

    def get_queryset(self):
        return Block.objects.all()



class BlockCreation(generics.CreateAPIView):
    serializer_class = BlockSerializer

    pagination_class = None

    def verifyBlockchain():
        pass

    def create(request, *args, **kwargs):
        pass
