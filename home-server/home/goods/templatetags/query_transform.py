from django import template

register = template.Library()

# https://stackoverflow.com/a/56824200/21973704
@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()