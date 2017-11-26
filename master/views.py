
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from master.master import Master
from common.models import Blockchain, Block, Transaction
from common.views import BlockchainGetView


class BlockchainView(BlockchainGetView):

    def get(self, request):
        """
        Example to see
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
        #data = Blockchain.serialize(blockchain)
        """

        data = Blockchain.serialize(Master.master.blockchain)
        print(Master.master.blockchain)

        return Response(data)

    def post(self, request):
        """
        Manage the POST request, the Master Node will receive a block and it
        will check wether it is accepted or not and will add it to the
        rest of the blockchain accordingly
        """

        try:
            block = Block.parse(request.data)
            isValid = self.verifyBlock(block)
            if isValid:
                Master.master.add_block_in_blockchain(block)
                data = Blockchain.serialize(Master.master.blockchain)
                response = Response({"Title":"Well played, your block has been added !", "data": data},
                                    status = status.HTTP_201_CREATED)
                # TODO Remove data from the answer, we just did it to check the evolution of the blockchain
            else:
                response = Response({"Title": "There is a problem"},status = status.HTTP_406_NOT_ACCEPTABLE)

        except Exception as e: # To change later since we're catching all exception and this might be a problem
            response = Response({"Title": "There is a problem"},status = status.HTTP_406_NOT_ACCEPTABLE)

        return response

    def verifyBlock(self,block): # Should we keep it here or outside the class or even in another file ?
        """
        Verify if the block data correspond to the current state of the blockchain
        """
        # Waiting for Miner's team part
        # For test sake, let's say it's alrdy checked
        isValid = True

        return isValid


class BlockView(APIView):

    def post(self, request):
        return Response("OK", status=201)