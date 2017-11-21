from django.db import models

# Create your models here.


class Block(models.Model):
    header = models.CharField(primary_key=True, max_length=256)  # SHA256 length
    nonce = models.IntegerField()

    class JSONAPIMeta:
        resource_name = "block"

    @classmethod
    def create(cls, header, nonce):
        block = cls(header=header, nonce=nonce)
        block.transactions = [Transaction(txid="TXID")]
        return block


class Transaction(models.Model):
    txid = models.CharField(primary_key=True, max_length=256) # SHA256 length
    amount = models.FloatField()
    receiver = models.CharField(max_length=256)
    sender = models.CharField(max_length=256)
    block_hash = models.CharField(max_length=256)
    timestamp = models.CharField(max_length=256)

    class JSONAPIMeta:
        resource_name = "transaction"
