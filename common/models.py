# from django.db import models
#
# import json
#
# class MyEncoder(json.JSONEncoder):
#     def default(self, o):
#         return o.__dict__
#
# class Block:
#
#     @staticmethod
#     def serialize():
#         pass
#
#     @staticmethod
#     def parse():
#         pass
#
#     def __init__(self):
#         self.header = str("Header value")
#         self.nonce = 187687697
#         self.transactions = [Transaction("Hello", 5), Transaction("Hello", 5)]
#
#
# class Transaction:
#     def __init__(self, txid, amount):
#         self.txid = txid
#         self.amount = amount
#
# # class Block(models.Model):
# #     header = models.CharField(max_length=256)  # SHA256 length
# #     nonce = models.IntegerField()
# #     # transaction = ArrayField()
# #     # def __init__(self, *args, **kwargs):
# #     #     super(models.Model, self).__init__(args, kwargs)
# #     #     self.transactions = []
# #
# #     class JSONAPIMeta:
# #         resource_name = "block"
# #
# #
# # class Transaction(models.Model):
# #     txid = models.CharField(primary_key=True, max_length=256) # SHA256 length
# #     amount = models.FloatField()
# #     receiver = models.CharField(max_length=256)
# #     sender = models.CharField(max_length=256)
# #     block_hash = models.CharField(max_length=256)
# #     timestamp = models.CharField(max_length=256)
# #
# #     class JSONAPIMeta:
# #         resource_name = "transaction"
