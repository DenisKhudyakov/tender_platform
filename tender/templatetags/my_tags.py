from django import template

register = template.Library()


@register.filter
def zip_lists(list1, list2):
    return zip(list1, list2)


@register.filter
def get(dictionary, key):
    return dictionary.get(key)
