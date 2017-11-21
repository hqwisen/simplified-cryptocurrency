from django.db import models


class Block(models.Model):
    header = models.CharField(max_length=256)  # SHA256 length
    nonce = models.IntegerField()
    # def __init__(self, *args, **kwargs):
    #     super(models.Model, self).__init__(args, kwargs)
    #     self.transactions = []

    class JSONAPIMeta:
        resource_name = "block"


class Transaction(models.Model):
    txid = models.CharField(primary_key=True, max_length=256) # SHA256 length
    amount = models.FloatField()
    receiver = models.CharField(max_length=256)
    sender = models.CharField(max_length=256)
    block_hash = models.CharField(max_length=256)
    timestamp = models.CharField(max_length=256)

    class JSONAPIMeta:
        resource_name = "transaction"