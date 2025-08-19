def cart_counts(request):
    cart = request.session.get('cart', {})
    qty = sum(item['qty'] for item in cart.values())
    return {'cart_count': qty}
