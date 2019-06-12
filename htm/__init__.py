import io
import re
import parser
import inspect
import functools
from tokenize import tokenize, untokenize
from token import tok_name

REX = re.compile(r"(?:\\{|[^{])*")


def split(string):
    strings = []
    exprs = []

    while True:
        match = REX.match(string)
        strings.append(match.group(0))
        if match.end() == len(string):
            break
        string = string[match.end() + 1 :]

        expr, string = parse_expr(string)
        exprs.append(compile(expr, "", "eval"))

    return strings, exprs


def parse_expr(string):
    b = string.encode("utf-8")
    sio = io.BytesIO(b)

    count = 0
    tokens = []
    for t in tokenize(sio.readline):
        if tok_name[t[0]] == "OP":
            if t[1] == "{":
                count += 1
            elif t[1] == "}":
                if count == 0:
                    row, offset = t[3]
                    sio.seek(0)
                    for _ in range(row - 1):
                        offset += len(sio.readline())
                    return (
                        untokenize(tokens).decode("utf-8"),
                        b[offset:].decode("utf-8"),
                    )
                count -= 1
        tokens.append(t)

    raise Exception()


RE_VALUE = re.compile(r"\"[^\"]*\"|'[^']*'|[^\"'>/\s]+")

RE_ATTR = re.compile(r"\"[^\"]*\"|'[^']*'|[^\"'>/=\s]+")

RE_WS = re.compile(r"\s*")


def get_token(string, start, regex):
    match = RE_ATTR.match(string, start)
    if not match:
        raise Exception()
    token = match.group(0)
    if token[0] in "\"'" and token[0] == token[-1]:
        token = token[1:-1]
    return token, match.end()


def skip_ws(string, start):
    match = RE_WS.match(string, start)
    return match.end()


def htm_parse(strings):
    ops = []
    text = True
    slash = False

    for index, string in enumerate(strings):
        start = 0
        while start < len(string):
            if text:
                found = string.find("<", start)
                if found == -1:
                    text = string[start:].strip()
                    if text:
                        ops.append(("CHILD", False, text))
                    if index < len(strings) - 1:
                        ops.append(("CHILD", True, index))
                    break

                if found == start:
                    start = start + 1
                else:
                    text = string[start:found].strip()
                    if text:
                        ops.append(("CHILD", False, text))
                    start = found + 1
                text = False

                start = skip_ws(string, start)
                if start >= len(string):
                    ops.append(("OPEN", True, index))
                elif string[start] == "/":
                    slash = True
                    start = start + 1
                    ops.append(("CLOSE",))
                elif string[start] != ">":
                    tag, start = get_token(string, start, RE_VALUE)
                    ops.append(("OPEN", False, tag))
                else:
                    raise Exception()
                continue

            start = skip_ws(string, start)
            if start >= len(string):
                raise Exception()

            if string[start] == ">":
                start = start + 1
                text = True
                slash = False
            elif string[start] == "/":
                if not slash:
                    ops.append(("CLOSE",))
                start = start + 1
                slash = True
            elif string[start : start + 3] == "..." and start + 3 == len(string):
                if not slash:
                    ops.append(("SPREAD", True, index))
                start = start + 3
            else:
                attr, start = get_token(string, start, RE_ATTR)

                next_ch = string[start : start + 1]
                if next_ch.isspace() or next_ch in ("/", ">"):
                    if not slash:
                        ops.append(("ATTR", attr, False, True))
                elif next_ch == "=":
                    start += 1
                    start = skip_ws(string, start)
                    if start >= len(string):
                        if not slash:
                            ops.append(("ATTR", attr, True, index))
                    else:
                        value, start = get_token(string, start, RE_VALUE)
                        if not slash:
                            ops.append(("ATTR", attr, False, value))
                else:
                    raise Exception(attr)

    count = 0
    for op in ops:
        if op[0] == "OPEN":
            count += 1
        elif op[0] == "CLOSE":
            count -= 1
        if count < 0:
            raise Exception("too many closes")
    if count > 0:
        raise Exception("too many opens")

    return ops


def htm_eval(h, ops, values, index=0):
    root = []
    stack = [("", {}, root)]

    for op in ops:
        if op[0] == "OPEN":
            _, value, tag = op
            stack.append((values[tag] if value else tag, {}, []))
        elif op[0] == "CLOSE":
            tag, props, children = stack.pop()
            stack[-1][2].append(h(tag, props, children))
        elif op[0] == "SPREAD":
            _, value, item = op
            tag, props, children = stack[-1]
            props.update(values[item] if value else item)
        elif op[0] == "ATTR":
            _, attr, value, item = op
            tag, props, children = stack[-1]
            props[attr] = values[item] if value else item
        elif op[0] == "CHILD":
            _, value, item = op
            tag, props, children = stack[-1]
            children.append(values[item] if value else item)
        else:
            raise Exception()

    if len(root) == 1:
        return root[0]
    return root


def htm(cache_size=128):
    def _htm(h):
        @functools.lru_cache(maxsize=cache_size)
        def parse(string):
            strings, exprs = split(string)
            ops = htm_parse(strings)
            return ops, exprs

        def html(string):
            ops, exprs = parse(string.strip())

            stack = inspect.stack()
            f_globals = stack[1].frame.f_globals
            f_locals = stack[1].frame.f_locals
            del stack

            values = []
            for expr in exprs:
                values.append(eval(expr, f_globals, f_locals))

            return htm_eval(h, ops, values)

        return html

    return _htm
