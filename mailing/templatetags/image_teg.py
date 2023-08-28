from django import template

register = template.Library()


@register.simple_tag()
def media_path(data):
    return data.url if data else '#'
