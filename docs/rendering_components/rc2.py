from h import html, render

name = 'World'

page = html("""
  <div>Hello {name}</div>
  """)

rc2 = render(page)
