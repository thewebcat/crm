from django import template

register = template.Library()

@register.filter(name='addattr')
def addattr(value, arg):
	arg_list = [item.strip() for item in arg.split(',')]
	return value.as_widget(attrs={arg_list[0]: arg_list[1]})