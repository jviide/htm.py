from htm import htm


@htm
def html(tag, props, children):
    return tag, props, children


result01 = html("""
  <div>Hello World</div>
""")
