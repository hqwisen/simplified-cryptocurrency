from django.db import models

# Create your models here.


class Block(models.Model):
    header = str()
    nonce = str()


class Transaction:

    def __init__(self):
        txid = str()
        amount = 0
        receiver = str()
        sender = str()
        block_hash = str()
        timestamp = str()
