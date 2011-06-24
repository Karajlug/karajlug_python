from django import template
from page import Page

from django import template

register = template.Library()

@register.navigation

def format_list(input_list):
return Page.objects.all()
