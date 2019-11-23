from htm import htm


@htm
def html(tag, props, children):
    return tag, props, children


# start
name = 'World'

result03 = html("""
  <div title="Say Hi">Hello {name}</div>
""")
