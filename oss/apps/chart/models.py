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
