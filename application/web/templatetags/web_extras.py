from django import template

register = template.Library()


@register.filter(name='chunk_evenly')
def chunk_evenly(value, chunk_size):
    a = iter(value)
    a = zip([iter(value)] * chunk_size)
    a = zip(*[iter(value)] * chunk_size)
    return zip(*[iter(value)] * chunk_size)
