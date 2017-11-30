from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common import client
from common.models import Block, Transaction, ParseException
from common.views import BlockchainGETView
from master.auth import RelayAuthentication
from master.master import Master


class BlockchainView(BlockchainGETView):
    authentication_classes = (RelayAuthentication,)
    permission_classes = (IsAuthenticated,)

    @property
    def server(self):
        return Master()


class BlockView(APIView):
    authentication_classes = (RelayAuthentication,)
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
            # request contains the block, and the address of the miner
            block_data = request.data['block']
            block = Block.parse(block_data)
        except ParseException as e:
            return Response({"Title": "There is a problem"},
                                status=status.HTTP_406_NOT_ACCEPTABLE)
        bad_transactions = self.server.update_blockchain(block)
        if len(bad_transactions) == 0:  # block is valid
            response = Response({"detail": "Block successfully added!"},
                                status=status.HTTP_201_CREATED)
            for relay_ip in settings.RELAY_IP:
                client.post(relay_ip, 'block', block_data)
        # TODO add reward to miner using request.data['miner_address']
        # client.post(relay_ip, 'transactions', transaction)
        else:
            data = {'bad_transactions': []}
            for transaction in bad_transactions:
                data['bad_transactions'].append(Transaction.serialize(transaction))
            response = Response({"errors": "Bad transactions where found in new block.",
                                 "data": data},
                                status=status.HTTP_406_NOT_ACCEPTABLE)
            # Send to all relays bad TXs, since the miner can request
            # transactions from any relay
            for relay_ip in settings.RELAY_IP:
                client.delete(relay_ip, 'transactions', data)
        return response
