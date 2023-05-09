from django.shortcuts import render
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.auth.models import User

# Create your views here.


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            user = request.user
            order = form.save(commit=False)
            order.user = user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'],
                
                )

            cart.clear()           
            return render(request, template_name='orders/order/created.html', context={'order': order})
    else:
        form = OrderCreateForm()
    return render(request, template_name='orders/order/create.html', 
                    context={
                        'form': form,
                        'cart': cart
                    }
            )