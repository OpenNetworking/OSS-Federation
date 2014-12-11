from django.db import models

# Create your models here.
class Tx(models.Model):
    tx_id = models.DecimalField(primary_key=True, max_digits=26, decimal_places=0)
    tx_hash = models.CharField(max_length=255)
    tx_type = models.IntegerField(blank=True, null=True)
    tx_color = models.DecimalField(max_digits=10, decimal_places=0, blank=True, null=True)
    total_in = models.DecimalField(max_digits=30, decimal_places=0)
    total_out = models.DecimalField(max_digits=30, decimal_places=0)
    tx_ntime = models.DecimalField(db_column='tx_nTime', max_digits=20, decimal_places=0, blank=True, null=True)  # Field name made lowercase.

class Block(models.Model):
    block_id = models.DecimalField(primary_key=True, max_digits=14, decimal_places=0)
    block_hash = models.CharField(unique=True, max_length=64)
    block_miner = models.CharField(db_column='block_miner', max_length=64, blank=True)  # Field name made lowercase.
    block_hashmerkleroot = models.CharField(db_column='block_hashMerkleRoot', max_length=64, blank=True)  # Field name made lowercase.
    block_ntime = models.DecimalField(db_column='block_nTime', max_digits=20, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    block_height = models.DecimalField(max_digits=14, decimal_places=0, blank=True, null=True)
