import io
import re
import parser
import inspect
import functools
from bisect import bisect
from tokenize import tokenize, untokenize
from token import tok_name

RE_TEMPLATE = re.compile(rb"(?:\\{|[^{])*")


class ParseError(ValueError):
    pass


def split(string):
    data = string.encode("utf-8")
    bio = io.BytesIO(data)

    row_offsets = [0]
    for line in data.split(b"\n"):
        row_offsets.append(row_offsets[-1] + len(line) + 1)

    strings = []
    exprs = []
    start = 0
    while True:
        match = RE_TEMPLATE.match(data, start)
        strings.append(match.group(0).decode("utf-8"))
        start = match.end()
        if start == len(data):
            break

        start = start + 1
        bio.seek(start)

        expr, row, column = parse_expr(bio)
        exprs.append(compile(expr, "", "eval"))

        start_row = bisect(row_offsets, start) - 1
        if row > 0:
            start = row_offsets[row + start_row] + column
        else:
            start = start + column

    return strings, exprs


def parse_expr(bio):
    count = 0
    tokens = []
    for t in tokenize(bio.readline):
        if tok_name[t[0]] == "OP":
            if t[1] == "{":
                count += 1
            elif t[1] == "}":
                if count == 0:
                    row, column = t[3]
                    return untokenize(tokens).decode("utf-8"), row - 1, column
                count -= 1
        tokens.append(t)
    raise ParseError("unterminated expression")


RE_VALUE = re.compile(r"\"[^\"]*\"|'[^']*'|[^\"'>/\s]+")

RE_ATTR = re.compile(r"\"[^\"]*\"|'[^']*'|[^\"'>/=\s]+")

RE_WS = re.compile(r"\s*")


def get_token(string, start, regex):
    match = RE_ATTR.match(string, start)
    if not match:
        raise ParseError("no token found")
    token = match.group(0)
    if token[0] in "\"'" and token[0] == token[-1]:
        token = token[1:-1]
    return token, match.end()


def skip_ws(string, start):
    match = RE_WS.match(string, start)
    return match.end()


def htm_parse(strings):
    ops = []
    in_tag = False
    slash = False

    for index, string in enumerate(strings):
        start = 0
        while start < len(string):
            if not in_tag:
                found = string.find("<", start)
                if found == -1:
                    text = string[start:].strip()
                    if text:
                        ops.append(("CHILD", False, text))
                    break

                text = string[start:found].strip()
                if text:
                    ops.append(("CHILD", False, text))
                start = found + 1
                in_tag = True

                start = skip_ws(string, start)
                if start >= len(string):
                    ops.append(("OPEN", True, index))
                    continue

                if string[start] == "/":
                    slash = True
                    start = start + 1
                    ops.append(("CLOSE",))
                elif string[start] != ">":
                    tag, start = get_token(string, start, RE_VALUE)
                    ops.append(("OPEN", False, tag))
                else:
                    raise ParseError("empty tag")

            start = skip_ws(string, start)
            if start >= len(string):
                if index == len(strings) - 1:
                    raise ParseError("unexpected end of data")
                raise ParseError("expression not allowed")

            if string[start] == ">":
                start = start + 1
                in_tag = False
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
                        if index == len(strings) - 1:
                            raise ParseError("unexpected end of data")
                        if not slash:
                            ops.append(("ATTR", attr, True, index))
                    else:
                        value, start = get_token(string, start, RE_VALUE)
                        if not slash:
                            ops.append(("ATTR", attr, False, value))
                elif next_ch:
                    raise ParseError("invalid character")
                elif index == len(strings) - 1:
                    raise ParseError("unexpected end of data")
                else:
                    raise ParseError("expression not allowed here")

        if not in_tag and index < len(strings) - 1:
            ops.append(("CHILD", True, index))

    count = 0
    for op in ops:
        if op[0] == "OPEN":
            count += 1
        elif op[0] == "CLOSE":
            count -= 1
        if count < 0:
            raise ParseError("closing unopened tags")
    if count > 0:
        raise ParseError("all opened tags not closed")
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
            raise BaseException("unknown op")

    if len(root) == 1:
        return root[0]
    return root


def htm(*, cache_maxsize=128):
    def _htm(h):
        @functools.lru_cache(maxsize=cache_maxsize)
        def parse(string):
            strings, exprs = split(string)
            ops = htm_parse(strings)
            return ops, exprs

        @functools.wraps(h)
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
