from django import template
import ast

register = template.Library()


@register.filter
def to_list(value):
    data=[ast.literal_eval(items) for items in value]
    return data