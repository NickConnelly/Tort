from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.simple_tag
def active(request, pattern):
    import re
    if re.search(pattern, request.path):
        return 'active'
    return ''

@register.simple_tag
def active_reverse(request, urls):
    if request.path in ( reverse(url) for url in urls.split() ):
        return "active"
    return ""
