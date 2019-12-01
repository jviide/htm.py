from htm import htm


@htm
def html(tag, props, children):
    return tag, props, children


# start
message = 'Say Howdy'
names = ['World', 'Universe', 'Galaxy']

result07 = html("""
  <ul title="{message}">
    {[
        html('<li>Hello {name}</li>')
        for name in names
     ] }
  </li>
""")
