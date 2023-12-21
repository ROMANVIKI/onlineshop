from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse



# Create your views here.

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            #clear the cart
            cart.clear()
            #Launch asynchronous task
            order_created.delay(order.id)

            #set the order in the session
            request.session['order_id'] = order.id
            
            #Store the form data in the session as well
            # request.session['order_form_data'] = {
            #     'first_name': form.cleaned_data['first_name'],
            #     'last_name': form.cleaned_data['last_name'],
            #     'email': form.cleaned_data['email'],
            #     'address': form.cleaned_data['address'],
            #     'postal_code': form.cleaned_data['postal_code'],
            #     'city': form.cleaned_data['city'],
            # }


            #redirect for payment
            return redirect(reverse('payment:process'))
        

            # return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})