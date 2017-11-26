
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from master.master import Master
from common.models import Blockchain, Block, Transaction, ParseException
from common.views import BlockchainGetView

USERNAME = "RelayNode" #The only user that can request something from the Master Node
#The password for this user is "RelayPwd123"
class BlockchainView(BlockchainGetView):


    def get(self, request):
        """
        Manage the GET request and will return the current state of the blockchain
        if the one requesting it is a Relay Node (see user and password above)
        """
        if is_auth(request.user):
            data = Blockchain.serialize(Master.master.blockchain)
            response = Response(data, status = status.HTTP_200_OK)
        else:
            response = Response(status = status.HTTP_403_FORBIDDEN)

        return response


    def post(self, request):
        """
        TO DELETE LATER
        USE THE POST REQUEST TO SEE HOW DOES A BLOCK LOOKS LIKE
        """
        if is_auth(request.user):
            transaction = Transaction()
            block = Block()
            block.add_transaction(transaction)
            tr = Transaction()
            tr.amount = 3
            block.add_transaction(tr)

            block2 = Block()
            tr2 = Transaction()
            tr2.amount = 3443
            block2.add_transaction(tr2)

            blockchain = Blockchain()
            blockchain.add_block(block)
            blockchain.add_block(block2)

            data = Block.serialize(block)

            response = Response(data, status = status.HTTP_200_OK)
        else:
            response = Response(status = status.HTTP_403_FORBIDDEN)
        return response


class BlockView(APIView):

    def post(self, request):
        """
        Manage the POST request, the Master Node will receive a block and it
        will check wether it is accepted or not and will add it to the
        rest of the blockchain accordingly only
        if the one requesting it is a Relay Node (see user and password above)

        """
        try:
            if is_auth(request.user):
                block = Block.parse(request.data)
                isValid = Master.master.verifyBlock(block)
                if isValid:
                    Master.master.add_block_in_blockchain(block)
                    data = Blockchain.serialize(Master.master.blockchain)
                    response = Response({"Title":"Well played, your block has been added !", "data": data}, status = status.HTTP_201_CREATED)
                    # TODO Remove data from the answer, we just did it to check the evolution of the blockchain
                else:
                    response = Response({"Title": "There is a problem"},status = status.HTTP_406_NOT_ACCEPTABLE)
            else:
                response = Response(status = status.HTTP_403_FORBIDDEN)


        except ParseException as e: # To change later since we're catching all exception and this might be a problem
            response = Response({"Title": "There is a problem"},status = status.HTTP_406_NOT_ACCEPTABLE)

        return response



def is_auth(user):
    """
    Verify if the user is allowed or not
    """
    flag = False
    if str(user) == USERNAME:
        flag = True

    return flag

