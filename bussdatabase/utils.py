def wikipedia_navn(link):
    import re
    import urllib.parse
    matches = re.match('.+wiki/(.+)', link)
    if not matches:
        return link

    link = matches.group(1).replace('_', ' ')
    link = urllib.parse.unquote_plus(link)
    return link


def can_edit(owner, current_user, perm):
    if owner == current_user:
        return True
    elif perm and current_user.has_perm(perm):
        return True
    else:
        return False
