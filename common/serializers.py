# from rest_framework import serializers
#
# from common.models import Block, Transaction
#
#
# class BlockSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Block
#         fields = '__all__'
#
#     def save(self, **kwargs):
#         return "Hello"
#
#     def serialize(self, block):
#         data = super.serialize(block)
#         data["transactions"] = []
#         for transaction in block.transactions:
#             data["transactions"].append(TransactionSerializer(transaction))
#         return data
#
#
# class TransactionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Transaction
#         fields = '__all__'
#
#
#
# def parse_block(data):
#     pass