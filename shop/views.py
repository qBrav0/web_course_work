from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Category, Product
from cart.forms import CartAddProductForm

# Create your views here.

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    paginator = Paginator(products, 12)  # Ограничение количества товаров на странице до 12
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        # Якщо параметр page не є цілим числом, виводимо першу сторінку
        page_obj = paginator.get_page(1)
    except EmptyPage:
        # Якщо номер сторінки більший, ніж загальна кількість сторінок, виводимо останню сторінку
        page_obj = paginator.get_page(paginator.num_pages)
    return render(request, 'shop/product/list.html', context={
        'category': category,
        'categories': categories,
        'products': page_obj,
    })
def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    product_images = product.images.all()

    return render(request, 'shop/product/detail.html', context={
        'product': product,
        'cart_product_form': cart_product_form,
        'product_images': product_images,
    })

def search(request):
    query = request.GET.get('q')
    if query:
        results = Product.objects.filter(name__icontains=query, available=True)
    else:
        results = []
    return render(request, 'shop/search.html', {'results': results, 'query': query})