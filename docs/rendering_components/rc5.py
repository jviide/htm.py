from h import html, render

name = 'World'


def heading(children, header="Components"):
    return html("""
        <h2>{header}</h2>
        {children}
    """)


page = html("""
  <{heading} header='My Components'>
      <div>Hello {name}</div>
  <//>
  """)

rc5 = render(page)
