from .cart import Cart
from django.conf import settings

def cart(request):
    return {'cart': Cart(request)}

