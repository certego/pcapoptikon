import hexdump
from django.template.defaultfilters import register


@register.filter("b64decode_hexdump")
def b64decode_hexdump(value, default=""):
    if isinstance(value, unicode):
        return hexdump.hexdump(
            value.decode('base64'),
            result='return'
        )
    elif isinstance(value, str):
        return hexdump.hexdump(
            unicode(value).decode('base64'),
            result='return'
        )
    else:
        return default
