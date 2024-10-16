from django.shortcuts import get_object_or_404, redirect
from .models import RedirectModel

def redirect_view(request, path):

    obj = get_object_or_404(RedirectModel, path=path)

    return redirect(obj.redirect_to)
