from htm import htm


@htm
def html(tag, props, children):
    return tag, props, children


# start
message = 'Say Howdy'
not_message = 'So Sad'
show_message = True

result08b = html("""
  <div>
    <h1>Show?</h1>
    {html('''<p>{message}</p>''') if show_message else html('''<p>{not_message}</p>''')}
  </div>
""")
