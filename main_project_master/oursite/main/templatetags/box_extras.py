from django import template
import time
import datetime
from dateutil.parser import parse

register = template.Library()

@register.simple_tag
def datefunction(dtime):
    return dtime
