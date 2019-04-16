from django import template

register = template.Library()


@register.filter
def wikipedia(link):
    import re
    import urllib.parse
    matches = re.match('.+wiki/(.+)', link)
    if not matches:
        return link

    link = matches.group(1).replace('_', ' ')
    link = urllib.parse.unquote_plus(link)
    return link
