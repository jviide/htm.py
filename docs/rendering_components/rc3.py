from h import html, render

name = 'World'

page = html("""
  <div editable>Hello {name}</div>
  """)

rc3 = render(page)
