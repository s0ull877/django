from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from django.core.cache import cache

from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory
from users.models import User


class IndexView(TitleMixin, TemplateView):

    template_name=r'products/index.html'
    title = 'Store'

    # context creating func
    def get_context_data(self, **kwargs) -> dict:

        context = super().get_context_data(**kwargs)
        context['is_promotion'] = True
        return context
     


class ProductsListViews(TitleMixin,ListView):

    model = Product
    template_name=r'products/products.html'
    paginate_by = 3
    title='Store - Каталог'
    

    def get_queryset(self):

        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')

        return queryset.filter(category__id=category_id) if category_id else queryset
    

    def get_context_data(self, **kwargs) -> dict:
        
        context = super().get_context_data()
        categories = cache.get('categories')

        if not categories:

            context['categories'] = ProductCategory.objects.all() 
            cache.set('categories',  context['categories'], 30)
        else:
            context['categories'] = categories

        return context
    

@login_required
def basket_add(request, product_id):
    
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)
    user = request.user

    if not baskets.exists():
        Basket.objects.create(user=user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])



