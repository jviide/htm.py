from hyperpython import h

from htm import htm


# start

@htm
def html(tag, props, children):
    if callable(tag):
        return tag()
    return h(tag, props, children)


def Heading():
    return html('<header>Hello World</header>')


result03 = str(html("""
    <{Heading}><//>
"""))
