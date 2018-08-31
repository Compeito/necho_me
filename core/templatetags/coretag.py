from django import template

from core.utils import created_at2str

register = template.Library()


@register.filter
def dt2str(arg):
    return created_at2str(arg)
