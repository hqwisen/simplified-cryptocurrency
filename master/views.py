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

import logging

logger = logging.getLogger(__name__)


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
            logger.debug("Block received from %s" % request.data['miner_address'])
            block_data = request.data['block']
            block = Block.parse(block_data)
        except KeyError:
            logger.debug("No block given.")
            return Response({"errors": "No block given."},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        except ParseException as e:
            logger.debug("Parsing block error.")
            return Response({"errors": "%s" % e},
                            status=status.HTTP_406_NOT_ACCEPTABLE)

        (hash_verify, bad_transactions) = self.server.update_blockchain(block)
        if hash_verify and len(bad_transactions) == 0:  # block is valid
            logger.debug("Block '%s' successfully added" % block.header)
            data = {'transactions': []}
            for transaction in block.transactions:
                data['transactions'].append(Transaction.serialize(transaction))
            for relay_ip in settings.RELAY_IP:
                logger.debug("Sending block '%s' to relay %s" % (block.header, relay_ip))
                client.post(relay_ip, 'blockchain', block_data)
                client.delete(relay_ip, 'transactions', data)
            if self.server.balance >= settings.REWARD:
                self.server.balance -= settings.REWARD
                miner_transaction = self.server.wallet.create_transaction(
                    request.data['miner_address'],
                    settings.REWARD)
                client.post(relay_ip, 'transactions', Transaction.serialize(miner_transaction))
            response = Response({"detail": "Block successfully added!"},
                                status=status.HTTP_201_CREATED)
        else:
            logger.debug("Block '%s' can NOT be added (bad header or bad TXs)." % block.header)
            data = {'transactions': []}
            if len(bad_transactions) > 0:
                for transaction in bad_transactions:
                    logger.debug("Bad TX '%s'" % transaction.hash)
                    data['transactions'].append(Transaction.serialize(transaction))
                # Send to all relays bad TXs, since the miner can request
                # transactions from any relay
                for relay_ip in settings.RELAY_IP:
                    logger.debug("Sending bad TXs to relay %s" % relay_ip)
                    client.delete(relay_ip, 'transactions', data)
                    response = Response({"errors": "Bad transactions where found in new block.",
                                         "data": data},
                                        status=status.HTTP_406_NOT_ACCEPTABLE)
            else:
                response = Response({"errors": "Bad header.",
                                     "data": block_data},
                                    status=status.HTTP_406_NOT_ACCEPTABLE)
        return response

    @property
    def server(self):
        return Master()
