import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import Block, ParseException, Blockchain
from relay.relay import Relay

from rest_framework import status

logger = logging.getLogger(__name__)


class BlockchainGetView(APIView):

    def get(self, request):
        blockchain = Relay.blockchain
        try:
            start, end = int(request.query_params['start']), int(request.query_params['end'])
            blockchain = Relay.part_of(start, end)
        except (KeyError, ValueError) as e:
            logger.info("Error while parsing params of GET blockchain; return all blockchain")
        data = Blockchain.serialize(blockchain)
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            block = Block.parse(request.data)
            Relay.update_blockchain(block)
            return Response(status=status.HTTP_201_CREATED)
        except ParseException as e:
            return Response(str(e), status=status.HTTP_406_NOT_ACCEPTABLE)


