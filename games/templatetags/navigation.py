from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.simple_tag
def navactive(topnav, pattern):
	import re
	if re.search(pattern, topnav):
		return 'active'
	return ''