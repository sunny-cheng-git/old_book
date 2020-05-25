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


#评分规则向下取整，再加半棵星
@register.simple_tag
def detail_star_numb(numb):
    print(numb)
    print(int(numb))
    print(isinstance(numb,float))
    ret = ''
    for i in range(int(numb)):
        ret+='<img src="/static/img/Star%20(Filled).png">'
    if isinstance(numb,float):
        ret+='<img src="/static/img/cc-star-half.png">'
    return mark_safe(ret)
