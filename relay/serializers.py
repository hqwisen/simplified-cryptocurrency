from rest_framework.serializers import ModelSerializer
from rest_framework.utils.serializer_helpers import ReturnDict

from relay.models import Block, Transaction



class BlockValidator(object):
    def __init__(self):
        pass

    def __call__(self, value):
        return "Validation"

class BlockSerializer(ModelSerializer):
    class Meta:
        model = Block
        validators = BlockValidator()
        fields = '__all__'

    @property
    def data(self):
        ret = super(ModelSerializer, self).data
        ret['transactions'] = []
        for transaction in self.instance.transactions:
            ret['transactions'].append(TransactionSerializer(transaction).data)
        return ReturnDict(ret, serializer=self)


class TransactionSerializer(ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
