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
    return tag_callable(**kwargs)


def Heading(header='Some Default', children=()):
    return html('<header>Hello {header}</header>')


result04 = str(html("""
    <{Heading} header='My Components'><//>
"""))
