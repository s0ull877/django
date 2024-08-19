from carts.models import HomeCart

def get_user_carts(request):

    if request.user.is_authenticated:
        return HomeCart.objects.filter(user=request.user).order_by('created').select_related('product')
    
    if not request.session.session_key:
        request.session.create()
    
    return HomeCart.objects.filter(session_key=request.session.session_key).order_by('created').select_related('product')
