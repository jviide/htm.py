from h import html, render

name = 'World'


def heading(header="Components"):
    return html("""
        <h2>{header}</h2>
    """)


page = html("""
  <{heading} header='My Components'><//>
  """)

rc4 = render(page)
