from hyperpython import h

from htm import htm


@htm
def html(tag, props, children):
    return h(tag, props, children)


# start
message = 'Say Howdy'
names = ['World', 'Universe', 'Galaxy']


def greeting(name):
    return html('<li>Hello {name}</li>')


result02 = str(html("""
  <ul title="{message}">
    {[greeting(name) for name in names]}
  </li>
"""))
