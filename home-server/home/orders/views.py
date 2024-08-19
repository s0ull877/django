import json
import uuid
from django.db import transaction

from django.forms import ValidationError

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.conf import settings

from yookassa import Configuration, Payment

from carts.utils import get_user_carts

from orders.forms import CreateOrderForm
from orders.models import Order, OrderItem


@login_required
def create_order(request):
    
    user_carts = get_user_carts(request)
    user = request.user

    if request.method == 'POST':

        form = CreateOrderForm(data=request.POST)

        if form.is_valid():
            try:
                with transaction.atomic():
                    if user_carts.exists():
                        
                        order = Order.objects.create(
                            user=user,
                            phone_number=form.cleaned_data['phone_number'],
                            requires_delivery=form.cleaned_data['requires_delivery'],
                            delivery_address=form.cleaned_data['delivery_address'],
                            payment_on_get=form.cleaned_data['payment_on_get'], 
                        )

                        for user_cart in user_carts:
                            product = user_cart.product
                            name = user_cart.product.name
                            price = user_cart.price
                            quantity = user_cart.quantity

                            if product.quantity < quantity:
                                raise ValidationError(f"Insufficient quantity of '{name}' in stock. \
                                                        In stock - {product.quantity}")
                            
                            OrderItem.objects.create(
                                order=order,
                                product=product,
                                name=name,
                                price=price,
                                quantity=quantity,
                            )

                            product.quantity -= quantity
                            product.save()

                        # Если оплата картой, редирект на юкассу
                        if form.cleaned_data['payment_on_get'] == '0':

                            payment = Payment.create({
                                "amount": {
                                    "value":user_carts.total_price(),
                                    "currency": "RUB" #не могу USD поставить изза account.gateway_id юкассы
                                },
                                "confirmation": {
                                    "type": "redirect",
                                    "return_url": "{}:8000{}".format(settings.DOMAIN_NAME, reverse('users:profile', kwargs={'pk':user.id}))
                                },
                                "capture": True,
                                "description": f"Заказ в Home #{order.id}",
                                'metadata': {
                                    'order_id': order.id
                                }
                            }, uuid.uuid4())

                            user_carts.delete()
                            return HttpResponseRedirect(payment.confirmation.confirmation_url)

                        user_carts.delete()
                        messages.success(request, 'Заказ оформлен!')
                        return redirect('users:profile', pk=user.id)
                    
            except ValidationError as e:
                messages.warning(request, str(e))
                return redirect('users:profile', pk=user.id)
    
            
        else:
            context = {'title': 'Home - Новый заказ', 'form': form}

            return render(request, 'orders/create_order.html', context)


        
    elif request.method == 'GET':

        if not user_carts.exists():
            
            messages.warning(request, f"Вы не можете оформить заказ, пока корзина пуста!")

            return redirect(to='goods:catalog', slug='all')

        
        else:

            init = {
                'first_name': user.first_name,
                'last_name': user.last_name
            }

            form = CreateOrderForm(initial=init)

            context = {'title': 'Home - Новый заказ', 'form': form}

            return render(request, 'orders/create_order.html', context)
        


Configuration.account_id = settings.YOKASSA_ACC_ID
Configuration.secret_key = settings.YOKASSA_SECRET
@csrf_exempt
def yookassa_webhook_view(request):

    payload = request.body.decode('utf-8')
    payload_dict = json.loads(payload)
    if payload_dict ['object']['status'] == 'succeeded':

        order_id = order_id = int(payload_dict['object']['metadata']['order_id'])
        order = Order.objects.get(id=order_id)
        order.is_paid = True
        order.save()

    elif payload_dict ['object']['status'] == 'canceled':

        # some func if pay canceled
        ...

    return HttpResponse(status=200)