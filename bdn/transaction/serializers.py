from rest_framework import serializers
from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = (
            'id',
            'transaction_type',
            'currency',
            'value',
            'date',
            'sender',
            'receiver',
            'tx_hash',
        )
