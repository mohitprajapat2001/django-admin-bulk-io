from django import template

register = template.Library()


@register.simple_tag
def render_model_fields(instance, field_name):
    return getattr(instance, field_name)
