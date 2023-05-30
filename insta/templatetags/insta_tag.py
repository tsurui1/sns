import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter()
def remove_tag(caption):
    # 「#」から始まる、1文字以上の文字列を空文字列に置き換えている
    return mark_safe(re.sub('#.+', '', caption))