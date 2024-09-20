from django import template

register = template.Library()    

@register.simple_tag(takes_context=True)
def clear_role(context, **kwargs):
    query = context['request'].GET.copy()
    try:
        query.pop('role')
    except KeyError:
        pass
    return query.urlencode()