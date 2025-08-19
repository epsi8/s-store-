from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Category, Product, Review
from cart.cart import Cart
from django.contrib import messages

def home(request):
    products = Product.objects.all().order_by('-created_at')[:12]
    categories = Category.objects.all()
    return render(request, 'home.html', {'products': products, 'categories': categories})

def search(request):
    q = request.GET.get('q', '')
    products = Product.objects.filter(Q(title__icontains=q) | Q(description__icontains=q)) if q else []
    return render(request, 'search_results.html', {'products': products, 'q': q})

def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = category.products.all()
    return render(request, 'category_list.html', {'category': category, 'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(category=product.category).exclude(id=product.id)[:8]
    cart = Cart(request)
    in_cart_qty = cart.get_quantity(product.id)
    return render(request, 'product_detail.html', {'product': product, 'related': related, 'in_cart_qty': in_cart_qty})

@login_required
def add_review(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        rating = int(request.POST.get('rating', '5'))
        comment = request.POST.get('comment', '')
        Review.objects.create(product=product, user=request.user, rating=rating, comment=comment)
        messages.success(request, 'Review added!')
    return redirect(product.get_absolute_url())
