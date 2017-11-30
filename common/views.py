import logging

from rest_framework.response import Response
from rest_framework.views import APIView

from common.models import Block, ParseException, Blockchain
from relay.relay import Relay

from rest_framework import status

logger = logging.getLogger(__name__)


class ViewUtils:

    @staticmethod
    def parse_int_param(params, key):
        """
        Parse a value and return the int value
        :param params: dict with all params
        :param key: key to access the required params
        :return: the int value or None if cannot parse it
        """
        try:
            param = int(params[key])
        except (KeyError, ValueError) as e:
            param = None
        return param

class BlockchainGETView(APIView):


    def get(self, request):
        start = ViewUtils.parse_int_param(request.query_params, 'start')
        end = ViewUtils.parse_int_param(request.query_params, 'end')
        return Response(Blockchain.serialize(self.server.part_of(start, end)),
                        status=status.HTTP_200_OK)

    @property
    def server(self):
        return None


