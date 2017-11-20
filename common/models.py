from django.db import models


class Block(models.Model):
    hash = models.CharField(max_length=256)  # SHA256 length
    hashPrevBlock = models.CharField(max_length=256)  # SHA256 length
    # nonce = models.IntegerField()

    class JSONAPIMeta:
        resource_name = "block"

class Transaction(models.Model):
    txid = models.CharField(max_length=256) # SHA256 length
    amount = models.FloatField()
    receiver = models.CharField(max_length=256)
    sender = models.CharField(max_length=256)
    blockHash = models.CharField(max_length=256)

    class JSONAPIMeta:
        resource_name = "transaction"
