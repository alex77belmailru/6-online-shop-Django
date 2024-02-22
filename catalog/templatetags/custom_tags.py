from django import template

register = template.Library()


@register.simple_tag
def mediapath(path_from_object):
    return path_from_object.url


@register.filter
def mediapath(path_from_object):
    return path_from_object.url
