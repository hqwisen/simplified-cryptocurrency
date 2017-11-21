from rest_framework import serializers

from common.models import Block, Transaction


class BlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Block
        fields = '__all__'

    def serialize(self, block):
        self.data["transactions"] = []
        for transaction in block.transactions:
            self.data["transactions"].append(TransactionSerializer(transaction))
        return self.data


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'



def parse_block(data):
    pass