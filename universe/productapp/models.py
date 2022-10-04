from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.

class UploadProduct_table(models.Model):
    
    prod_category = [
        ("---------", "--------"),
        ("Fashion", "Fashion"),
        ("Electronics", "Electronics"),
        ("Computers", "Computers"),

    ]

    product_id = models.AutoField(primary_key=True)
    user =  models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    product_name = models.CharField(unique=True, max_length=50)
    date_upload = models.DateTimeField(default=timezone.now)
    quantity = models.CharField(unique=False, max_length=11)
    price = models.CharField(unique=False, max_length=11)
    description = models.CharField(unique=False, max_length=100)
    product_picture = models.ImageField(upload_to='productImage/', unique=False)
    category = models.CharField(choices=prod_category, unique=False, max_length=50, null=True)
    display = models.BooleanField(default=False, unique=False)
    approve_status = models.CharField(unique=False, max_length=100, default='Unapproved')


class Order_table(models.Model):
    order_id = models.AutoField(primary_key=True)
    date_ordered = models.DateTimeField(default=timezone.now)
    product = models.ForeignKey(UploadProduct_table, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(unique=False)
    price = models.CharField(unique=False, max_length=11)
    purchased = models.BooleanField(default=False, unique=False)
    delivered = models.BooleanField(default=False, unique=False)
    delivery_agent = models.IntegerField(unique= False, null=True)