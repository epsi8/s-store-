from store.models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product_id, qty=1, update=False):
        product_id = str(product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {'qty': 0}
        if update:
            self.cart[product_id]['qty'] = qty
        else:
            self.cart[product_id]['qty'] += qty
        self.save()

    def remove(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        self.session['cart'] = {}
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for p in products:
            item = self.cart[str(p.id)]
            item['product'] = p
            item['total'] = p.price * item['qty']
            yield item

    def get_total(self):
        return sum(item['product'].price * item['qty'] for item in self)

    def get_quantity(self, product_id):
        return self.cart.get(str(product_id), {}).get('qty', 0)

    def save(self):
        self.session.modified = True
