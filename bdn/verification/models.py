from django.db import models as m


class Verification(m.Model):
    tx_hash = m.CharField(max_length=70)
    block_hash = m.CharField(max_length=70)
    block_number = m.IntegerField(default=0)
    granted_to = m.CharField(max_length=42)
    ipfs_hash = m.CharField(max_length=50)
    date_created = m.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tx_hash
