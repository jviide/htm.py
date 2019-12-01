from htm import htm
from hyperpython import h


@htm
def html(tag, props, children):
    return h(tag, props, children)


result01 = str(html("""
  <div>Hello World</div>
"""))
