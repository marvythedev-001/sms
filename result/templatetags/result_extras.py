from django import template

register = template.Library()


@register.filter(name='get_item')
def get_item(dictionary, key):
    if dictionary is None:
        return None
    try:
        return dictionary.get(key)
    except Exception:
        try:
            return dictionary[key]
        except Exception:
            return None


# alias to tolerate the misspelling 'get_iteme' if used in templates
register.filter('get_item', get_item)
