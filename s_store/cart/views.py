from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from store.models import Product
from .cart import Cart
from .models import WishItem

def view_cart(request):
    cart = Cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})

def add_to_cart(request, product_id):
    cart = Cart(request)
    qty = int(request.POST.get('qty', 1)) if request.method == 'POST' else 1
    cart.add(product_id, qty=qty)
    messages.success(request, 'Added to cart')
    product = get_object_or_404(Product, id=product_id)
    return redirect(product.get_absolute_url())

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    messages.info(request, 'Removed from cart')
    return redirect('view_cart')

@login_required
def wishlist(request):
    items = WishItem.objects.filter(user=request.user).select_related('product')
    return render(request, 'cart/wishlist.html', {'items': items})

@login_required
def add_wishlist(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    WishItem.objects.get_or_create(user=request.user, product=product)
    messages.success(request, 'Added to wishlist')
    return redirect(product.get_absolute_url())

@login_required
def remove_wishlist(request, product_id):
    WishItem.objects.filter(user=request.user, product_id=product_id).delete()
    messages.info(request, 'Removed from wishlist')
    return redirect('wishlist')
