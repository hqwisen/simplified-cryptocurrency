import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import Block, ParseException, Blockchain
from relay.relay import Relay

from rest_framework import status

logger = logging.getLogger(__name__)


class BlockchainGetView(APIView):

    def get(self, request):
        server = self.get_server()
        if server is None:
            raise Exception("Cannot instanciate server.")
        try:
            start, end = int(request.query_params['start']), int(request.query_params['end'])
            blockchain = server.part_of(start, end)
        except (KeyError, ValueError) as e:
            logger.info("No start, end given return full blockchain.")
            blockchain = server.get_blockchain()
        data = Blockchain.serialize(blockchain)
        return Response(data, status=status.HTTP_200_OK)

    def get_server(self):
        return None


