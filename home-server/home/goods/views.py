from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView


from common.views import TitleMixin

from goods.models import Products, Categories
from goods.utils import q_search



class ProductsListView(TitleMixin, ListView):

    model = Products
    template_name = "goods/catalog.html"
    title = 'Home - Каталог'
    paginate_by = 6


    def get_context_data(self, **kwargs) -> dict:
        
        context = super().get_context_data(**kwargs)
        return context

    
    def get_queryset(self):

        queryset = super().get_queryset()
        
        slug = self.kwargs.get('slug')
        if slug:
            try:
                products = Categories.objects.get(slug=slug).products_set.all()
            except Categories.DoesNotExist:
                return Products.objects.none()
        else:
            products = Categories.objects.get(slug='all').products_set.all()

        
        params = self.request.GET
        query = params.get('q')
        if query:
            products = q_search(query)

        if params.get('on_sale'):
            products = products.filter(discount__gt=0)

        if params.get('order_by'):
            products = products.order_by(params.get('order_by'))
        else:
            products = products.order_by('id')


        return products
    


class ProductDetailView(TitleMixin, DetailView):

    model = Products
    template_name = "goods/product.html"
    title = 'Home - Продукт'


    




