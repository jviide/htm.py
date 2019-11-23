from htm import htm
from html import escape as _escape
from collections import namedtuple
from collections.abc import Iterable, ByteString
from inspect import signature, Parameter

H = namedtuple("H", ["tag", "props", "children"])


@htm
def html(tag, props, children):
    children = tuple(flatten(children))
    if callable(tag):
        return relaxed_call(tag, children=children, **props)
    return H(tag, props, children)


def flatten(value):
    if isinstance(value, Iterable) and not isinstance(value, (H, str, ByteString)):
        for item in value:
            yield from flatten(item)
    else:
        yield value


def relaxed_call(callable_, **kwargs):
    # Hackety-hack-hack warning!
    # Call callable_ with the given keyword arguments, but
    # only those that callable_ expects - ignore others.

    sig = signature(callable_)
    parameters = sig.parameters

    if not any(p.kind == p.VAR_KEYWORD for p in parameters.values()):
        extra_key = "_"
        while extra_key in parameters:
            extra_key += "_"

        sig = sig.replace(
            parameters=[*parameters.values(), Parameter(extra_key, Parameter.VAR_KEYWORD)])
        kwargs = dict(sig.bind(**kwargs).arguments)
        kwargs.pop(extra_key, None)

    return callable_(**kwargs)


def render(value):
    return "".join(render_gen(value))


def render_gen(value):
    for item in flatten(value):
        if isinstance(item, H):
            tag, props, children = item
            yield f"<{escape(tag)}"
            if props:
                yield f" {' '.join(encode_prop(k, v) for (k, v) in props.items())}"

            if children:
                yield ">"
                yield from render_gen(children)
                yield f'</{escape(tag)}>'
            else:
                yield f'/>'
        elif item not in (True, False, None):
            yield escape(item)


def escape(value):
    return _escape(str(value))


def encode_prop(k, v):
    if v is True:
        return escape(k)
    return f'{escape(k)}="{escape(v)}"'
