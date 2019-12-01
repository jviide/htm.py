from inspect import signature, Parameter

from hyperpython import h

from htm import htm


# start

@htm
def html(tag, props, children):
    if callable(tag):
        # In this case:
        #   props={'header': 'My Components'}
        return tag_factory(tag, children=children, **props)
    return h(tag, props, children)


def tag_factory(tag_callable, **kwargs):
    sig = signature(tag_callable)
    parameters = sig.parameters

    # Pick through the callable's signature and get
    # what is needed
    if not any(p.kind == p.VAR_KEYWORD for p in parameters.values()):
        extra_key = "_"
        while extra_key in parameters:
            extra_key += "_"

        sig = sig.replace(
            parameters=[*parameters.values(),
                        Parameter(extra_key, Parameter.VAR_KEYWORD)
                        ]
        )
        kwargs = dict(sig.bind(**kwargs).arguments)
        kwargs.pop(extra_key, None)

    return tag_callable(**kwargs)


def Heading(header='Some Default'):
    return html('<header>Hello {header}</header>')


result05 = str(html("""
    <{Heading} header='My Components' unused=9><//>
"""))
