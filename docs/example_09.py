from htm import htm
from hyperpython import h
from inspect import signature, Parameter


@htm
def html(tag, props, children):
    if callable(tag):
        return relaxed_call(tag, children=children, **props)
    return h(tag, props, children)


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

        sig = sig.replace(parameters=[*parameters.values(), Parameter(extra_key, Parameter.VAR_KEYWORD)])
        kwargs = dict(sig.bind(**kwargs).arguments)
        kwargs.pop(extra_key, None)

    return callable_(**kwargs)


class HyperpythonComponent:
    def __hyperpython__(self):
        return html("""<h2>Hyperpython components!</h2>""")


def greeting(children, header="Functional components!"):
    return html("""
    <h2>{header}</h2>
    <ul>
      {children}
    </ul>
  """)


result09 = html("""
    <div>
      <h1>Hello Python</h1>
      <p>Now you can write HTML in Python!</p>
      <!-- also with components -->
      <{HyperpythonComponent} />
      <!-- and functional components -->
      <{greeting}>
        <li>foo</li>
        <li>bar</li>
      <//>
    </div>
  """)
