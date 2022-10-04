from django import forms
from .models import UploadProduct_table, Order_table


class UploadProduct_form(forms.ModelForm):
    class Meta:
        model = UploadProduct_table
        fields = [
            'product_name',
            'quantity',
            'price',
            'description',
            'category',
            'product_picture'
        ]

        widgets = {
            'description': forms.Textarea(attrs={'cols':100, 'row': 10})
        }


class Product_Quantity_form(forms.ModelForm):
    class Meta:
        model = Order_table
        fields = [
            'quantity'
        ]
