from htm import htm


@htm
def html(tag, props, children):
    return tag, props, children


# start
message = 'Say Howdy'
name = 'World'

result04 = html("""
  <div title="{message}">Hello {name}</div>
""")
