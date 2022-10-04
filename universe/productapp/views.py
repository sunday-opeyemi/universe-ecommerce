from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from .forms import UploadProduct_form, Product_Quantity_form
from .models import UploadProduct_table, Order_table
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.db import transaction

# Create your views here.

@login_required
def uploadProduct(request):
    if request.method == 'POST':
        product_form = UploadProduct_form(request.POST or None, request.FILES or None)
        if product_form.is_valid():
            product_name = product_form.cleaned_data['product_name']  
            price = product_form.cleaned_data['price']
            quantity = product_form.cleaned_data['quantity']
            description = product_form.cleaned_data['description']
            picture = product_form.cleaned_data['product_picture']
            category = product_form.cleaned_data['category']

            post = UploadProduct_table(product_name=product_name, quantity=quantity, price=price, description=description, product_picture = picture, category=category)

            post.user_id = request.user.id
            post.save()   

            messages.success(request, ('Product successfully uploaded!'))
            return HttpResponseRedirect("upload_product")
        else:
            messages.error(request, ('Please correct the error below.'))
            return HttpResponseRedirect('upload_product')
    else:
        product_form = UploadProduct_form()
        return render(request, 'productapp/uploadproduct_form.html', {
        'uploadproduct_form': product_form,    
        })
    
@login_required
def displayProduct(request):
    product_details = UploadProduct_table.objects.all()
    return render(request, 'productapp/displayProduct.html', {'productDetails':product_details})

@login_required
def approveProduct(request, product_id):  
    product = UploadProduct_table.objects.get(product_id=product_id)
    if product.approve_status == "Unapprove":
        product.approve_status = "Approved"
    else:
        product.approve_status = "Unapprove"
    product.save()
    return displayProduct(request)

@login_required
def editProduct(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(UploadProduct_table, product_id=product_id)
        uploadProduct_form = UploadProduct_form(request.POST or None, request.FILES or None, instance=product)
        if uploadProduct_form.is_valid():
            uploadProduct_form.save()
            messages.success(request, ('Product was successfully updated!'))
            return displayProduct(request)
        else:
            messages.error(request, ('Please correct the error below.'))
            return HttpResponseRedirect('edit_product')
    else:
        product = get_object_or_404(UploadProduct_table, product_id=product_id)
        product_form = UploadProduct_form(instance=product)
        return render(request, 'productapp/edit_product_form.html', {
        'product_form': product_form,    
        })

@login_required
def marketPlace(request):
    product = UploadProduct_table.objects.all().filter(display=True)
    return render(request, 'index.html', {'product':product})

@login_required
def moreProduct(request, category):
    product = UploadProduct_table.objects.all().filter(category=category)
    return render(request, 'productapp/moreProduct.html', {'product':product})

@login_required
def productDetails(request, product_id):
    if request.method == 'POST':
        product_form = Product_Quantity_form(request.POST)
        if product_form.is_valid():  
            quantity = product_form.cleaned_data['quantity']

            post = Order_table(product_id=product_id, quantity=quantity, user_id=request.user.id )
            product = UploadProduct_table.objects.get(product_id=product_id)
            price = float(quantity) * float(product.price)
            post.price = price
            post.save()   

            messages.success(request, ('Item added to cart!'))
            return HttpResponsePermanentRedirect(reverse('product_details', args=(product_id)))
        else:
            messages.error(request, ('Please correct the error below.'))
            return HttpResponsePermanentRedirect(reverse('product_details', args=(product_id)))
    else:  
        quantity_form = Product_Quantity_form()
        product = UploadProduct_table.objects.all().filter(product_id=product_id)
        return render(request, 'productapp/productDetails.html', {'product':product, 'quantity_form': quantity_form})

@login_required
def viewMyCart(request, user_id):
    product = Order_table.objects.all().filter(user_id=user_id, purchased=False)
    return render(request, 'productapp/viewCart.html', {'product':product})

@login_required
def editMyCart(request, product_id):
    product = UploadProduct_table.objects.all().filter(product_id=product_id)
    if request.method == 'POST':
        product_instance = get_object_or_404(Order_table, product_id=product_id)
        product_form =  Product_Quantity_form(request.POST, instance=product_instance)
        if product_form.is_valid():
            new_price = float(product.values()[0].get("price")) * float(product_form.cleaned_data["quantity"])
            new_quantity = product_form.cleaned_data["quantity"]
            Order_table.objects.filter(product_id=product_id).update(quantity=new_quantity, price=new_price)
            messages.success(request, ('Product successfully updated to cart!'))
            return viewMyCart(request, request.user.id)
        else:
            messages.error(request, ('Please correct the error below.'))
            return HttpResponsePermanentRedirect(reverse('product_details', args=(product_id)))
    else:
        product_instance = get_object_or_404(Order_table, product_id=product_id)
        product_form = Product_Quantity_form(instance=product_instance)
        return render(request, 'productapp/editCart_form.html', 
            {'product_form': product_form, 'product':product})

@login_required
def removeFromCart(request, product_id):
    Order_table.objects.filter(product_id=product_id).delete()
    messages.success(request, ('Product successfully deleted from cart!'))
    return viewMyCart(request, request.user.id)