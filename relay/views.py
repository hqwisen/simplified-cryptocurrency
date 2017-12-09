import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from common import client
from common.models import Block, Transaction, ParseException, Blockchain
from common.views import BlockchainGETView
from relay.relay import Relay, RelayError

from django.conf import settings

logger = logging.getLogger(__name__)


class BlockchainView(BlockchainGETView):
    def post(self, request):
        # TODO make sure that only master node can request this
        try:
            block = Block.parse(request.data)
        except ParseException as e:
            return Response({'errors': str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)
        logger.debug("Adding block '%s' to blockchain" % block.header)
        updated = self.server.update_blockchain(block)
        # TODO test when the blockchain is not updated
        if not updated:
            logger.debug("Blockchain not up to date, requesting part of.")
            response = client.get(settings.MASTER_IP,
                                  'blockchain?start=%d' % (self.server.blockchain_size - 1))
            blockchain = Blockchain.parse(response.data)
            self.server.add_blocks(blockchain.blocks)
        return Response(status=status.HTTP_201_CREATED)

    @property
    def server(self):
        return Relay()


class BlockView(APIView):
    def post(self, request):
        logger.debug("Receive a block, forwarding to master.")
        user = settings.RELAY_CREDENTIALS['username']
        pwd = settings.RELAY_CREDENTIALS['password']
        response = client.post(settings.MASTER_IP, 'block', request.data, basic_auth=(user, pwd))
        # TODO what to return to miner ?
        return Response(status=status.HTTP_200_OK)


class TransactionView(APIView):
    def get(self, request):
        server = Relay()
        if 'exclude_hash' in request.data:
            exclude = request.data['exclude_hash']
        else:
            exclude = []
            logger.debug("'exclude_hash' not in request.")
        transaction = server.get_transaction(exclude)
        if transaction is not None:
            return Response(Transaction.serialize(transaction),
                            status=status.HTTP_200_OK)
        else:
            return Response({'errors': 'no transaction to send'},
                            status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        """
        Add a new transaction to the relay transactions list.
        If the transaction.hash is already in the list,
        it will not be added and return 406
        :param request:
        :return: 201 if transaction added, 406 otherwise (hash already exist)
        """
        server = Relay()
        try:
            transaction = Transaction.parse(request.data)
            server.add_transaction(transaction)
            return Response(status=status.HTTP_201_CREATED)
        except (RelayError, ParseException) as e:
            return Response(str(e), status=status.HTTP_406_NOT_ACCEPTABLE)

    def delete(self, request):
        """
        Delete transactions receive in request.data['transactions']
        This is usually done when masternode receive an incorrect block
        and reject some transaction.

        :param request:
        :return: 2OO (OK)
        """
        # TODO make sure that only masters can request deletes
        server = Relay()
        for tx_data in request.data['transactions']:
            try:
                transaction = Transaction.parse(tx_data)
            except ParseException as e:
                logger.warning("Cannot remove transaction: %s" % (str(e)))
            else:
                logger.debug("Removing transaction %s " % transaction.hash)
            server.remove_transaction(transaction)
        return Response(status=status.HTTP_200_OK)
