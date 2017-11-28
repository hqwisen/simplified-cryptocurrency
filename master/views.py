from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from master.master import Master
from common.models import Blockchain, Block, Transaction, ParseException
from common.views import BlockchainGetView

USERNAME = "RelayNode"  # The only user that can request something from the Master Node


# The password for this user is "RelayPwd123"

class BlockchainView(BlockchainGetView):
    def get_server(self):
        return Master()

    def get(self, request):
        """
        Manage the GET request and will return the current state of the blockchain
        if the one requesting it is a Relay Node (see user and password above)
        """
        server = Master()
        if is_auth(request.user):
            super(BlockchainView, self).get(request)
        # data = Blockchain.serialize(Master.master.blockchain)
        #     response = Response(data, status = status.HTTP_200_OK)
        else:
            response = Response(status=status.HTTP_403_FORBIDDEN)

        return response


class BlockView(APIView):
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
            if is_auth(request.user):
                server = self.get_server()
                block = Block.parse(request.data)
                bad_transactions = server.update_blockchain(block)
                if len(bad_transactions) == 0: # block is valid
                    response = Response({"Title": "Well played, your block has been added !"},
                                        status=status.HTTP_201_CREATED)
                    # TODO envoyer block a tout les relays
                else:
                    data = {'trasactions': []}
                    for transaction in bad_transactions:
                        data['transactions'].append(Transaction.serialize(transaction))
                    response = Response({"errors": "Houston, there is a problem.", "data": data},
                                        status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                response = Response(status=status.HTTP_403_FORBIDDEN)


        except ParseException as e:  # To change later since we're catching all exception and this might be a problem
            response = Response({"Title": "There is a problem"}, status=status.HTTP_406_NOT_ACCEPTABLE)

        return response


def is_auth(user):
    """
    Verify if the user is allowed or not
    """
    flag = False
    if str(user) == USERNAME:
        flag = True

    return flag
