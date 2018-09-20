import uuid
from enum import IntEnum
from django.db import models as m


class TransactionType(IntEnum):
    DEPOSIT = 1
    WITHDRAW = 2


class Transaction(m.Model):
    id = m.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction_type = m.PositiveSmallIntegerField(
        default=TransactionType.WITHDRAW,
        choices=[(_.value, _.name) for _ in TransactionType])
    currency = m.CharField(max_length=3, default='EDU')
    value = m.FloatField()
    date = m.DateTimeField(auto_now=True)
    sender = m.CharField(max_length=42)
    receiver = m.CharField(max_length=42)
    tx_hash = m.CharField(max_length=70, null=True, blank=True)

    def __str__(self):
        return self.tx_hash
