from django import template

register = template.Library()

@register.simple_tag
def loop_range(start, end):
    return range(start, end + 1)

@register.simple_tag
def fill_range(start, end):
    l = ""
    for i in range(start, end):
        l.append(i)
        
    return l


@register.simple_tag
def division(a, b):
    if b == 0:
        return "Divisão por zero não é possível"
    return a / b
