from django import template

register = template.Library()

import calendar
@register.filter
def month_name(month_number):
    return calendar.month_name[month_number][:3]
    
@register.filter
def bcol(count):
    """Returns Twitter bootstrap column css classes for a responsive design"""
    if count == 1:
      css_classes = 'col-lg-12 col-md-12'
    elif count == 2:
      css_classes = 'col-lg-6 col-md-12'
    elif count == 3:
      css_classes = 'col-lg-4 col-md-6'
    elif count == 4:
      css_classes = 'col-lg-3 col-md-6'
    elif count == 5:
      css_classes = 'col-lg-4 col-md-6'
    else:
      css_classes = 'col-lg-3 col-md-6'
    return css_classes
