from htm import htm


@htm
def html(tag, props, children):
    return tag, props, children


# start
message = 'Say Howdy'
name = 'World'

result06 = html("""
  <section>
    <div title="{message}">Hello {name.upper()}</div>
  </section>
""")
