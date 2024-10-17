from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from .models import RedirectModel

def redirect_view(request, path):

    obj = get_object_or_404(RedirectModel, path=path)

    RedirectModel.objects.filter(pk=obj.id).update(redirect_count=F('redirect_count')+1)

    return redirect(obj.redirect_to)
