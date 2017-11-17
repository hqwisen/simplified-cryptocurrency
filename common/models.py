from django.db import models


class Block(models.Model):
    hash = models.CharField(max_length=256) # SHA256 length

    class JSONAPIMeta:
        resource_name = "block"
