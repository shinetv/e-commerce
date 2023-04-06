
from django.shortcuts import get_object_or_404, redirect, render
from numpy import product
from dazzlesapp.models import *
from .models import Cart,CartItem
from django.core.exceptions import ObjectDoesNotExist
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

# Create your views here.

def _cart_id(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart

def add_cart(request,product_id):
    product=Product.objects.get(id=product_id)
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart=Cart.objects.create(
            cart_id=_cart_id(request)
        )
        cart.save()
    try:
        cart_item=CartItem.objects.get(product=product,cart=cart)
        if cart_item.quantity < cart_item.product.stock:
            cart_item.quantity +=1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item=CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        cart_item.save()
    return redirect('my_cart:cart_detail')

def cart_detail(request,total=0,counter=0,cart_items=None):
    client = razorpay.Client(auth=("rzp_test_q7avKBVVBhaerO", "K4AzgJi0WWJ4uPImygiLAP3U"))
    cart=Cart.objects.get(cart_id=_cart_id(request))
    cart_items=CartItem.objects.filter(cart=cart,active=True)
    DATA = {
    "amount": 30000,
    "currency": "INR"
   
    
   
    
    }
    client.order.create(data=DATA)
    try:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_items=CartItem.objects.filter(cart=cart,active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            counter +=cart_item.quantity
    except ObjectDoesNotExist:
        pass
    return render(request,'cart.html',dict(cart_items=cart_items,total=total,counter=counter))

@csrf_exempt
def success(request):
    return render(request,'success.html')


def remove(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    if cart_item.quantity >1:
        cart_item.quantity -=1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('my_cart:cart_detail')

def Total_remove(request,product_id):
    cart=Cart.objects.get(cart_id=_cart_id(request))
    product=get_object_or_404(Product,id=product_id)
    cart_item=CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('my_cart:cart_detail')


