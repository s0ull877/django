import json
import uuid

from yookassa import Payment,Configuration

from django.conf import settings
from django.urls import reverse_lazy
from django.http import HttpResponse

from django.views.generic.edit import CreateView 
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView

from django.views.generic.list import ListView

from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import HttpResponseRedirect,reverse

from products.context_processors import baskets

from orders.models import Order


from common.views import TitleMixin

from orders.forms import OrderForm    

Configuration.account_id = settings.YOKASSA_ACC_ID
Configuration.secret_key = settings.YOKASSA_SECRET

class OrderSuccess(TitleMixin,TemplateView):
    template_name = "orders/success.html"
    title = 'Store - Спасибо за заказ'


class OrderCreateViews(TitleMixin, CreateView):

    template_name = 'orders/order-create.html'
    title = 'Store - Оформление заказа'
    form_class = OrderForm
    success_url = reverse_lazy('orders:order_create')
    
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)

        user_basket = baskets(request)

        payment = Payment.create({
            "amount": {
                "value": user_basket['baskets'].total_sum(),
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": "{}{}".format(settings.DOMAIN_NAME, reverse('orders:succeeded'))
            },
            "capture": True,
            "description": f"Заказ в Store #{self.object.id}",
            'metadata': {
                'order_id': self.object.id
            }
        }, uuid.uuid4())

        return HttpResponseRedirect(payment.confirmation.confirmation_url)

    def form_valid(self, form):

        form.instance.initiator = self.request.user
        return super().form_valid(form)
    

class OrdersListView(TitleMixin,ListView):
    model = Order
    title = 'Store - Заказы'
    template_name = "orders/orders.html"
    queryset = Order.objects.all()
    ordering = ('-id')


    def get_queryset(self):
        
        queryset = super().get_queryset()
        return queryset.filter(initiator=self.request.user)


class OrderListView(TitleMixin,ListView):

    model = Order
    title = f'Store - Заказ'
    template_name = "orders/order.html"
    queryset = Order.objects.all()
    ordering = ('-id')

    def get_context_data(self, **kwargs) -> dict:
        
        context = super().get_context_data()
        order_id = self.kwargs.get('order_id')

        try:
            context['order'] = Order.objects.filter(initiator=self.request.user, id=order_id)[0]
        except IndexError:
            answer = {'pass': True, 'id': order_id}
            context['order'] = answer

        return context


class OrderDetailView(TitleMixin,DetailView):

    model = Order
    template_name = "orders/order.html"
    title = f'Store - Заказ'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context['pass'] = False
        
        if self.request.user == context['order'].initiator:
            context['pass'] = True

        return context

    


@csrf_exempt
def yookassa_webhook_view(request):
    
    payload = request.body.decode('utf-8')
    payload_dict = json.loads(payload)
    # status = payload_dict['object']['status']

    order_id = int(payload_dict['object']['metadata']['order_id'])
    try:
        
        order = Order.objects.get(id=order_id)

        if not order.status:
            order.update_after_payment()

    except Order.DoesNotExist:
        pass

    return HttpResponse(status=200)


