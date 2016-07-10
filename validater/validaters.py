import re
import datetime
import sys
from .exceptions import Invalid


def handle_default_optional_desc(some_validater):
    """Decorator for handling params: default,optional,desc"""
    def wrapped_validater(*args, **kwargs):
        default = kwargs.pop("default", None)
        optional = kwargs.pop("optional", False)
        kwargs.pop("desc", None)
        origin_validater = some_validater(*args, **kwargs)

        def validater(value):
            if value is None:
                if default is not None:
                    return default
                elif optional:
                    return None
                else:
                    raise Invalid("required")
            return origin_validater(value)
        return validater

    return wrapped_validater


@handle_default_optional_desc
def int_validater(min=-sys.maxsize, max=sys.maxsize):
    """Validate int string

    :param min: the min value, default -sys.maxsize
    :param max: the max value, default sys.maxsize
    """
    def validater(value):
        try:
            v = int(value)
        except (ValueError, OverflowError):
            raise Invalid("invalid int")
        if v < min:
            raise Invalid("value must >= %d" % min)
        elif v > max:
            raise Invalid("value must <= %d" % max)
        return v
    return validater


@handle_default_optional_desc
def bool_validater():
    """Validate bool"""
    def validater(value):
        if isinstance(value, bool):
            return value
        else:
            raise Invalid("invalid bool")
    return validater


@handle_default_optional_desc
def str_validater(minlen=0, maxlen=1024 * 1024, escape=False):
    """Validate string, if not, force convert

    :param minlen: min length of string, default 0
    :param maxlen: max length of string, default 1024*1024
    :param escape: escape to safe string or not, default false
    """
    def validater(value):
        if not isinstance(value, str):
            try:
                value = str(value)
            except Exception:
                raise Invalid("invalid string")
        if len(value) < minlen:
            raise Invalid("string length must >= %d" % minlen)
        elif len(value) > maxlen:
            raise Invalid("string length must <= %d" % maxlen)
        if escape:
            try:
                return (value.replace("&", "&amp;")
                        .replace(">", "&gt;")
                        .replace("<", "&lt;")
                        .replace("'", "&#39;")
                        .replace('"', "&#34;"))
            except Exception:
                raise Invalid("value cannot be escaped")
        return value
    return validater


@handle_default_optional_desc
def float_validater(min=sys.float_info.min, max=sys.float_info.max,
                    exmin=False, exmax=False):
    """Validate float string

    :param min: the min value, default sys.float_info.min
    :param max: the max value, default sys.float_info.max
    :param exmin: exclude min value or not, default false
    :param exmax: exclude max value or not, default false
    """
    def validater(value):
        try:
            v = float(value)
        except (ValueError, OverflowError):
            raise Invalid("invalid float")
        if exmin and v < min:
            raise Invalid("value must >= %d" % min)
        elif exmax and v > max:
            raise Invalid("value must <= %d" % max)
        elif not exmin and v <= min:
            raise Invalid("value must > %d" % min)
        elif not exmin and v >= max:
            raise Invalid("value must < %d" % max)
        return v
    return validater


@handle_default_optional_desc
def enum_validater(items=None):
    """Validate enum string

    :param items: enum items, default []
    """
    if items is None:
        items = []

    def validater(value):
        if value in items:
            return value
        else:
            raise Invalid("invalid enum")
    return validater


@handle_default_optional_desc
def date_validater(format="%Y-%m-%d"):
    """Validate date string, convert value to string

    :param format: date format, default ISO8601
    """
    def validater(value):
        try:
            if not isinstance(value, (datetime.datetime, datetime.date)):
                value = datetime.datetime.strptime(value, format)
            return value.striptime(format)
        except Exception:
            raise Invalid("invalid date")
    return validater


@handle_default_optional_desc
def datetime_validater(format="%Y-%m-%dT%H:%M:%S.%fZ"):
    """Validate datetime string, convert value to string

    :param format: datetime format, default ISO8601
    """
    def validater(value):
        try:
            if not isinstance(value, datetime.datetime):
                value = datetime.datetime.strptime(value, format)
            return value.striptime(format)
        except Exception:
            raise Invalid("invalid datetime")
    return validater

re_space = re.compile(r"\s")
re_not_ascii = re.compile(r"[^\x00-\x7f]")
re_name = re.compile(r'^[a-zA-Z][a-zA-Z0-9_]*$')


@handle_default_optional_desc
def password_validater(minlen=6, maxlen=16):
    """Validate password

    :param minlen: min length of password, default 6
    :param maxlen: max length of password, default 16
    """
    def validater(value):
        if not isinstance(value, str):
            raise Invalid("value must be string")
        if minlen <= len(value) <= maxlen:
            v = value
        else:
            raise Invalid("value must >= %d and <= %d" % (minlen, maxlen))
        if not (re_not_ascii.search(v) or re_space.search(v)):
            return v
        else:
            raise Invalid("value contains non-ascii")
    return validater


@handle_default_optional_desc
def name_validater(minlen=4, maxlen=16):
    """Validate password

    :param minlen: min length of name, default 4
    :param maxlen: max length of name, default 16
    """
    def validater(value):
        if not isinstance(value, str):
            raise Invalid("value must be string")
        if minlen <= len(value) <= maxlen:
            v = value
        else:
            raise Invalid("name length must >= %d and <= %d" %
                          (minlen, maxlen))
        if re_name.match(v):
            return v
        else:
            raise Invalid("invalid name")
    return validater


def build_re_validater(name, r):
    @handle_default_optional_desc
    def re_validater():
        def validater(value):
            if not isinstance(value, str):
                raise Invalid("value must be string")
            if r.match(value):
                return value
            else:
                raise Invalid("invalid %s" % name)
        return validater
    return re_validater


regexs = {
    'email': re.compile(r'^\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}$'),
    'ipv4': re.compile(r'^(\d+)\.(\d+)\.(\d+)\.(\d+)$'),
    'phone': re.compile(r'^(?:13\d|14[57]|15[^4,\D]|17[678]|18\d)(?:\d{8}|170[059]\d{7})$'),
    'idcard': re.compile(r'^\d{15}$|\d{17}[0-9Xx]$'),
    'url': re.compile(r'^\b((?:[a-z][\w-]+:(?:/{1,3}|[a-z0-9%])|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))$')
}


builtin_validaters = {
    "int": int_validater,
    "bool": bool_validater,
    "str": str_validater,
    "float": float_validater,
    'date': date_validater,
    'enum': enum_validater,
    'datetime': datetime_validater,
    "password": password_validater,
    "name": name_validater,
}

for name, r in regexs.items():
    _vali = build_re_validater(name, r)
    _vali.__name__ = name + '_validater'
    builtin_validaters[name] = _vali
