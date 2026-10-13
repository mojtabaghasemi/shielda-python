from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def shielda_scripts():
    url = getattr(settings, "SHIELDA_WIDGET_URL", "https://shielda.ir/widget/api.js")
    return mark_safe(f'<script src="{url}" async defer></script>')


@register.simple_tag
def shielda_widget(theme="auto", lang="fa"):
    site_key = getattr(settings, "SHIELDA_SITE_KEY", "")
    return mark_safe(
        f'<div class="darban-captcha" data-sitekey="{site_key}" '
        f'data-theme="{theme}" data-lang="{lang}"></div>'
    )
