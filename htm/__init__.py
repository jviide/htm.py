import re
import functools
from tagged import tag, ParseError


RE_COLLAPSE = re.compile(r"^[^\S\n]*\n\s*|[^\S\n]*\n\s*$")


def collapse_ws(string):
    return RE_COLLAPSE.sub("", string)


def get_simple_token(scanner, regex):
    match = scanner.match(regex)
    if not match:
        raise ParseError("no token found")
    token = match.group(0)
    if token[0] in "\"'" and token[0] == token[-1]:
        token = token[1:-1]
    return token


class Scanner:
    def __init__(self, strings):
        self._strings = strings
        self._index = 0
        self._start = 0

    def peek(self):
        if self._index < len(self._strings):
            if self._start < len(self._strings[self._index]):
                return True, self._strings[self._index][self._start]
            if self._index < len(self._strings) - 1:
                return False, self._index
        return False, None

    def pop(self):
        is_text, value = self.peek()
        if is_text:
            self._start += 1
        elif value is not None:
            self._index += 1
            self._start = 0
        return is_text, value

    def match(self, regex):
        if self._index < len(self._strings):
            match = regex.match(self._strings[self._index], self._start)
            if match:
                self._start = match.end()
                return match
        return None

    def search(self, regex):
        start = self._start
        prefix = []
        for index in range(self._index, len(self._strings)):
            match = regex.search(self._strings[index], start)
            if match:
                if start < match.start():
                    prefix.append((True, self._strings[index][start:match.start()]))
                self._index = index
                self._start = match.end()
                return match, tuple(prefix)
            if start < len(self._strings[index]):
                prefix.append((True, self._strings[index][start:]))
            if index < len(self._strings) - 1:
                prefix.append((False, index))
            start = 0
        return None, ()

    def flush(self):
        flushed = []
        start = self._start
        for index in range(self._index, len(self._strings)):
            if start < len(self._strings[index]):
                flushed.append((True, self._strings[index][start:]))
            if index < len(self._strings) - 1:
                flushed.append((False, index))
            start = 0
        self._index = len(self._strings)
        self._start = 0
        return tuple(flushed)


TAG_OR_COMMENT_START = re.compile(r"<(?:!--|/)?")
COMMENT_END = re.compile(r"-->")
TAG_NAME = re.compile(r"\"[^\"]*\"|'[^']*'|[^\"'>/\s]+")
PROP_NAME = re.compile(r"\"[^\"]*\"|'[^']*'|[^\"'>/=\s]+")
WHITESPACE = re.compile(r"\s*")
SPREAD = re.compile(r"\.\.\.")
TAG_END = re.compile(r"/?>")
DOUBLE_QUOTE = re.compile(r"\"")
SINGLE_QUOTE = re.compile(r"'")
PROP_VALUE_END = re.compile(r"(?=/>|>|\s)")


def htm_parse(strings):
    scanner = Scanner(strings)

    ops = []
    while True:
        match, prefix = scanner.search(TAG_OR_COMMENT_START)
        for is_text, value in (prefix if match else scanner.flush()):
            if is_text:
                value = collapse_ws(value)
                if value:
                    ops.append(("CHILD", False, collapse_ws(value)))
            else:
                ops.append(("CHILD", True, value))
        if not match:
            break

        if match.group(0) == "<!--":
            match, _ = scanner.search(COMMENT_END)
            if not match:
                raise ParseError("missing comment end")
            continue

        elif match.group(0) == "</":
            slash = True
        else:
            slash = False
            is_text, value = scanner.peek()
            if is_text:
                tag = get_simple_token(scanner, TAG_NAME)
                ops.append(("OPEN", False, tag))
            elif value is not None:
                scanner.pop()
                ops.append(("OPEN", True, value))
            else:
                raise ParseError("unexpected end of data")

        while True:
            scanner.match(WHITESPACE)
            is_text, value = scanner.peek()
            if not is_text:
                if value is None:
                    raise ParseError("unexpected end of data")
                raise ParseError("expression not allowed")

            match = scanner.match(TAG_END)
            if match:
                if match.group(0) == "/>":
                    slash = True
                if slash:
                    ops.append(("CLOSE",))
                slash = False
                break

            match = scanner.match(SPREAD)
            in_text, value = scanner.peek()
            if match and not in_text and value is not None:
                _, index = scanner.pop()
                if not slash:
                    ops.append(("SPREAD", True, index))
                continue

            prop = get_simple_token(scanner, PROP_NAME)
            is_text, value = scanner.peek()
            if not is_text:
                if value is None:
                    raise ParseError("unexpected end of data")
                raise ParseError("expression not allowed here")

            if value.isspace() or value in ("/", ">"):
                if not slash:
                    ops.append(("PROP_SINGLE", prop, False, True))
            elif value == "=":
                scanner.pop()

                is_text, value = scanner.peek()
                if is_text and value == "\"":
                    scanner.pop()
                    match, prefix = scanner.search(DOUBLE_QUOTE)
                elif is_text and value == "'":
                    scanner.pop()
                    match, prefix = scanner.search(SINGLE_QUOTE)
                else:
                    match, prefix = scanner.search(PROP_VALUE_END)

                if not match:
                    raise ParseError("unexpected end of data")

                if not prefix:
                    ops.append(("PROP_SINGLE", prop, False, ""))
                elif len(prefix) == 1:
                    is_text, value = prefix[0]
                    ops.append(("PROP_SINGLE", prop, not is_text, value))
                else:
                    ops.append(("PROP_MULTI", prop, prefix))
            else:
                raise ParseError("invalid character")

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
        elif op[0] == "PROP_SINGLE":
            _, attr, value, item = op
            tag, props, children = stack[-1]
            props[attr] = values[item] if value else item
        elif op[0] == "PROP_MULTI":
            _, attr, items = op
            tag, props, children = stack[-1]
            props[attr] = "".join(value if is_text else str(values[value]) for (is_text, value) in items)
        elif op[0] == "CHILD":
            _, value, item = op
            tag, props, children = stack[-1]
            children.append(values[item] if value else item)
        else:
            raise BaseException("unknown op")

    if len(root) == 1:
        return root[0]
    return root


def htm(func=None, *, cache_maxsize=128):
    cached_parse = functools.lru_cache(maxsize=cache_maxsize)(htm_parse)

    def _htm(h):
        @tag
        @functools.wraps(h)
        def __htm(strings, values):
            ops = cached_parse(strings)
            return htm_eval(h, ops, values)
        return __htm

    if func is not None:
        return _htm(func)
    return _htm
