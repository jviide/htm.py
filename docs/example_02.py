from htm import htm


@htm
def html(tag, props, children):
    return tag, props, children


# start
name = 'World'

result02 = html("""
  <div>Hello {name}</div>
""")
