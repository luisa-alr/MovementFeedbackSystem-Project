from pylsl import *
import unicodedata
import re

def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')




def prettyPrintFormat(format):
    if format == cf_float32:
        return "Float 32bit"
    if format == cf_double64:
        return "Double 64bit"
    if format == cf_string:
        return "String"
    if format == cf_int32:
        return "Integer 32bit"
    if format == cf_int16:
        return "Integer 16bit"
    if format == cf_int8:
        return "Integer 8bit"
    if format == cf_int64:
        return "Integer 64bit"
    else:
        return "Undefined"