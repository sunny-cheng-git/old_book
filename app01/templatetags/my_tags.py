#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Sunny"
# Date: 2020-05-18


from django import template
from django.utils.safestring import mark_safe

register = template.Library()  # register的名字是固定的,不可改变


@register.simple_tag
def star_numb(numb):
    ret = ''
    for i in range(numb):
        ret+='<span class="glyphicon glyphicon-star-empty"></span>'
    return mark_safe(ret)




