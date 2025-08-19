from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.cart import Cart
from .models import Order, OrderItem
from decimal import Decimal
from django.conf import settings
import razorpay

@login_required
def checkout(request):
    cart = Cart(request)
    if cart.get_total() == 0:
        messages.error(request, 'Your cart is empty.')
        return redirect('home')

    # Create local order (we will attach razorpay ids after creating RZP order)
    total = Decimal(cart.get_total())
    order = Order.objects.create(user=request.user, total=total)

    # Create Razorpay order if keys present
    rzp_order = None
    if settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET:
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        rzp_order = client.order.create({
            "amount": int(total * 100),
            "currency": "INR",
            "payment_capture": 1,
            "notes": {"order_id": str(order.id)}
        })
        order.razorpay_order_id = rzp_order.get("id", "")
        order.save()

    # Prepare items (we will persist after successful payment)
    items_preview = list(cart)

    return render(request, 'orders/checkout.html', {
        "order": order,
        "items": items_preview,
        "rzp_key_id": settings.RAZORPAY_KEY_ID,
        "rzp_order": rzp_order,
    })

@login_required
def success(request):
    # In real flow, verify signature. Here we accept POST from Razorpay success handler.
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        payment_id = request.POST.get('razorpay_payment_id')
        try:
            order = Order.objects.get(id=order_id, user=request.user)
        except Order.DoesNotExist:
            return redirect('home')

        order.payment_id = payment_id or ''
        order.status = 'paid'
        order.save()

        # Move cart items into OrderItems
        from cart.cart import Cart
        from store.models import Product
        cart = Cart(request)
        for item in cart:
            OrderItem.objects.create(
                order=order,
                product=item['product'],
                price=item['product'].price,
                qty=item['qty']
            )
        cart.clear()

        from django.contrib import messages
        messages.success(request, 'Payment successful! Order placed.')
        return redirect('profile')

    return redirect('home')
