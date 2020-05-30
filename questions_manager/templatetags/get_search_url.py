from django import template

register = template.Library()


@register.simple_tag
def get_url(request, field, value):
    query_string = request.GET.copy()
    query_string[field] = value

    return query_string.urlencode()
