from django.db import models
from django.contrib.auth.models import User
from universe.productapp.models import UploadProduct_table, Order_table
from django.utils import timezone

# Create your models here.

class Invoice_table(models.Model):
    invoice_id = models.AutoField(primary_key=True)
    date_cashout = models.DateTimeField(default=timezone.now, unique=False)
    order_user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    total_price = models.CharField(unique=False, max_length=11)
    cashout = models.BooleanField(default=False, unique=False)
    delivery_agent = models.IntegerField(unique= False, default=0)
    delivered = models.BooleanField(default=False, unique=False)

class Product_Invoice_table(models.Model):
    proInv_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(UploadProduct_table, on_delete=models.CASCADE, unique=False)
    invoice = models.ForeignKey(Invoice_table, on_delete=models.CASCADE, unique=False)
    order_user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    product_price = models.CharField(unique=False, max_length=11)