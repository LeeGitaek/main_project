from django import template
import time
import datetime


register = template.Library()

@register.simple_tag
def getvalue(d):
    return d
