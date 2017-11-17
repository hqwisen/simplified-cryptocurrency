import logging

from django.contrib.auth.models import AnonymousUser
from rest_framework import generics
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import IsAuthenticated

from common.models import Block
from common.serializers import BlockSerializer

logger = logging.getLogger(__name__)


class BlockCollection(generics.ListAPIView):
    model_class = Block
    serializer_class = BlockSerializer
    # TODO Build a pagination for part of blockchain request
    pagination_class = None

    def get_queryset(self):
        return Block.objects.all()