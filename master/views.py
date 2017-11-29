from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, BaseAuthentication
from rest_framework.permissions import IsAuthenticated

from common import client
from master.master import Master
from common.models import Blockchain, Block, Transaction, ParseException
from common.views import BlockchainGETView

USERNAME = "RelayNode"  # The only user that can request something from the Master Node


# The password for this user is "RelayPwd123"

class CustomAuthentication(BaseAuthentication):

    def authenticate(self, request):
        if request.user.is_relay:
            return (request.user, None)
        else:
            return None

class BlockchainView(BlockchainGETView):


    authentication_classes = (CustomAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_server(self):
        return Master()

    # def get(self, request):
    #     """
    #     Manage the GET request and will return the current state of the blockchain
    #     if the one requesting it is a Relay Node (see user and password above)
    #     """
    #     server = Master()
    #     if is_auth(request.user):
    #         super(BlockchainView, self).get(request)
    #     # data = Blockchain.serialize(Master.master.blockchain)
    #     #     response = Response(data, status = status.HTTP_200_OK)
    #     else:
    #         response = Response(status=status.HTTP_403_FORBIDDEN)
    #
    #     return response


class BlockView(APIView):

    authentication_classes = (CustomAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """
        Manage the POST request, the Master Node will receive a block and it
        will check wether it is accepted or not and will add it to the
        rest of the blockchain accordingly only
        if the one requesting it is a Relay Node (see user and password above).
        If the block is rejected because of bad transactions, those transactions
        are returned to the relay node that made the request.
        If the block is accepted, the new block is sent to all relay nodes.
        """
        try:
            server = self.get_server()
            # request contains the block, and the address of the miner
            block_data = request.data['block']
            block = Block.parse(block_data)
            bad_transactions = server.update_blockchain(block)
            if len(bad_transactions) == 0: # block is valid
                response = Response({"Title": "Well played, your block has been added !"},
                                    status=status.HTTP_201_CREATED)
                for relay_ip in settings.RELAY_IP:
                    client.post(relay_ip, 'block', block_data)
            # TODO add reward to miner using request.data['miner_address']
            # client.post(relay_ip, 'transactions', transaction)

            else:
                data = {'bad_transactions': []}
                for transaction in bad_transactions:
                    data['bad_transactions'].append(Transaction.serialize(transaction))
                response = Response({"errors": "Houston, there is a problem.", "data": data},
                                    status=status.HTTP_406_NOT_ACCEPTABLE)
                # Need to send to all relays, since the miner can request
                # transactions from any relay
                for relay_ip in settings.RELAY_IP:
                    client.delete(relay_ip, 'transactions', data)

        except ParseException as e:
            response = Response({"Title": "There is a problem"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return response