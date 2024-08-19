from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from carts.models import HomeCart
from carts.utils import get_user_carts

from goods.models import Products


def basket_add_item(request):
    
    product_id = request.POST.get('product_id')

    product = Products.objects.get(id=product_id)

    if request.user.is_authenticated:
        carts = HomeCart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.last()
            cart.quantity += 1
            cart.save()
        
        else:
            HomeCart.objects.create(user=request.user,product=product)

    else: 
        carts = HomeCart.objects.filter(session_key=request.session.session_key, product=product)

        if carts.exists():
            cart = carts.last()
            cart.quantity += 1
            cart.save()
        
        else:
            HomeCart.objects.create(session_key=request.session.session_key, product=product)

    user_carts = get_user_carts(request)
    cart_items_html = render_to_string(
        'carts/includes/included_cart.html', {'carts': user_carts}, request=request
    )

    response_data = {
        'message': 'Товар добавлен в корзину',
        'cart_items_html': cart_items_html
    }

    return JsonResponse(response_data)



def basket_delete_item(request):
    
    cart_id = request.POST.get('cart_id')
    cart = HomeCart.objects.get(id=cart_id)
    quantity_deleted = cart.quantity
    cart.delete()

    user_carts = get_user_carts(request)
    cart_items_html = render_to_string(
        'carts/includes/included_cart.html', {'carts': user_carts}, request=request
    )

    response_data = {
        'message': 'Товар удален из корзины',
        'cart_items_html': cart_items_html,
        'quantity_deleted': quantity_deleted
    }

    return JsonResponse(response_data)



def basket_change(request):
    
    cart_id = request.POST.get('cart_id')
    quantity = request.POST.get('quantity')

    cart = HomeCart.objects.get(id=cart_id)

    cart.quantity = quantity
    cart.save()

    user_carts = get_user_carts(request)
    cart_items_html = render_to_string(
        'carts/includes/included_cart.html', {'carts': user_carts}, request=request
    )

    response_data = {
        'message': 'Количество изменено',
        'cart_items_html': cart_items_html,
        'quantity': quantity
    }

    return JsonResponse(response_data)
