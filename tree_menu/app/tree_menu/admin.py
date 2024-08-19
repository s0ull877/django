from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from tree_menu.models import Category, SubCategory



class ParentNameListFilter(admin.SimpleListFilter):

    title = _("Parent Name")

    parameter_name = "parent__name"

    def lookups(self, request, model_admin):
        
        category_id = request.GET.get('category__id__exact')
        subcategories = SubCategory.objects.filter(url='').filter(category__id=category_id).order_by('id') if category_id else SubCategory.objects.filter(url='').order_by('id')
        return [(str(subcategory.name), _(str(subcategory.name))) for subcategory in subcategories]


    def queryset(self, request, queryset):
                 
        if not self.value():
            return queryset
        
        
        parent_name = self.value()
        queryset = queryset.filter(parent__name=parent_name).order_by('id')
        return queryset
         
        

class SubCategoryAdminTab(admin.TabularInline):
    
    verbose_name = 'Дочерняя категория'
    verbose_name_plural = 'Дочерние категории'
    model=SubCategory
    ordering = ('id',)
    list_display = ('name', 'url', 'parent',)
    fields = ( 'name', 'url', 'parent',)
    search_fields = ('name',)
    readonly_fields = ('id', 'category')
    extra=0

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        str_id = request.path.split('/')[4]
        
        if request.path.split('/')[3] == 'category':
            kwargs["queryset"] = SubCategory.objects.filter(category__id=int(str_id))
        elif request.path.split('/')[3] == 'subcategory':
            kwargs["queryset"] = SubCategory.objects.filter(parent__id=int(str_id))
        else:
            db = kwargs.get("using")
            queryset = self.get_field_queryset(db, db_field, request)
            if queryset is not None:
                kwargs["queryset"] = queryset

        return super().formfield_for_foreignkey(db_field, request, **kwargs)




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
        
        list_display=(
            'name',
            'description',
        )
        list_filter = ('id','name')
        search_fields = ('id','name',)
        inlines = (SubCategoryAdminTab,)



@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    
    list_display =  (
        'name',
        'parent',
        'url',
        'category',
    )
    list_filter = (ParentNameListFilter, 'category')
    inlines = (SubCategoryAdminTab,)
