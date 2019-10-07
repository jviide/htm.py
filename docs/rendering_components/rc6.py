from h import html, render

name = 'World'


def heading(children, header="Todos"):
    return html("""
        <h2>{header}</h2>
        {children}
    """)


def todo_list(items):
    for text in items:
        yield html("<li>{text}</li>")


page = html("""
  <{heading} header='My Todos'>
    <ul>
      <{todo_list} items={('foo', 'bar')}><//>
    </ul>  
  <//>
  """)

rc6 = render(page)
