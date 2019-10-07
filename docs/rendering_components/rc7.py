from h import html, render

name = 'World'

footer_message = 'The Footer'  # Could be None


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
  {footer_message and html("<footer>{footer_message}<//>")}
  """)

rc7 = render(page)
