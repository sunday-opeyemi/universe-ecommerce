from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from .models import Invoice_table, Product_Invoice_table
from universe.productapp.models import Order_table
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.db import transaction
from django.core.mail import send_mail
import random


# Create your views here.
price = 0
@login_required
@transaction.atomic
def checkoutFromCart(request, user_id):
    global price
    price = 0
    product_ordered = Order_table.objects.all().filter(user_id=user_id, purchased=False)
    # check_invoice = Product_Invoice_table.objects.all().filter(user_id=user_id, purchased=False) 
    email = User.objects.only("email").filter(id=request.user.id).values()[0].get("email")

    if product_ordered:
        product_details = product_ordered.values()
        for product in product_details:
            price += float(product.get("price"))

        checkout = Invoice_table(order_user_id=user_id, total_price=price)
        checkout.save()

        for product in product_details:
            ordered_product = Product_Invoice_table(product_id=product.get("product_id"), invoice_id=checkout.invoice_id, order_user_id=product.get("user_id"),  product_price=product.get("price"))
            ordered_product.save()
        
        return render(request, "paymentapp/receipt.html", {"email":email, "product_invoice":product_ordered, "total_price":price, "invoice_id":checkout.invoice_id})
    else:
        messages.error(request, ('You have not order any item in your cart!'))
        return render(request, "productapp/viewCart.html")

@login_required
@transaction.atomic
def paymentSuccess(request, invoice_id):
    # Atter payment is successful then update Invoice_table and ordered_product
    Invoice_table.objects.all().filter(invoice_id=invoice_id).update(cashout=True)
    product_ordered = Order_table.objects.all().filter(user_id=request.user.id, purchased=False).values()
    # attach order to a staff
    staff = User.objects.all().filter(is_staff=True, is_superuser=False).values()
    _id = random.randint(0, len(staff)-1)
    staff_id = staff[_id].get("id")
    for product in product_ordered:
        Order_table.objects.all().filter(order_id=product.get("order_id")).update(purchased=True, delivery_agent=staff_id)
        Invoice_table.objects.all().filter(invoice_id=invoice_id).update(delivery_agent=staff_id)

    # send mail to the staff
    send_mail(
        'An order is available',# Subject of the mail
        'A customer with the ID:'+str(staff_id)+" just made an order \n Check the order details and make a package of the delivery.", # Body of the mail
        'ogunleyekolade@yahoo.com', # From email (Sender)
        [staff[_id].get("email")], # To email (Receiver)
        fail_silently=False, # Handle any error
    )

    messages.success(request, ('Your payment was successful!')) 
    return render(request, "paymentapp/successpay.html")

def paymentFail(request, invoice_id):
    messages.error(request, ('Transaction fails!'))
    return render(request, "paymentapp/successpay.html")

def trackOrder(request, user_id):
    product_ordered = Invoice_table.objects.all().filter(delivery_agent=user_id, delivered=False, cashout=True)
    return render(request, "paymentapp/delivered_product.html", {"product_invoice":product_ordered})

def productInvoice(request, invoice_id):
    product_ordered = Product_Invoice_table.objects.all().filter(invoice_id=invoice_id)
    return render(request, "paymentapp/ordered_details.html", {"product_invoice":product_ordered})

def productDelivered(request, invoice_id):
    Invoice_table.objects.all().filter(invoice_id=invoice_id).update(delivered=True)
    return trackOrder(request, request.user.id)