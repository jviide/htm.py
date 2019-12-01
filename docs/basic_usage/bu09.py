from htm import htm


@htm
def html(tag, props, children):
    return tag, props, children


# start
message = 'Say Howdy'
names = ['World', 'Universe', 'Galaxy']


def greeting(name):
    return html('<li>Hello {name}</li>')


result09 = html("""
  <ul title="{message}">
    {[greeting(name) for name in names]}
  </li>
""")
