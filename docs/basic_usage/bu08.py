from htm import htm


@htm
def html(tag, props, children):
    return tag, props, children


# start
message = 'Say Howdy'
not_message = 'So Sad'
show_message = True

result08 = html("""
    <h1>Show?</h1>
    {message if show_message else not_message}
""")
