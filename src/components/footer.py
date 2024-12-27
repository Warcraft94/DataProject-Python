from dash import html

def get_footer():
  """Returns the footer component."""
  return html.Footer(
      id="footer",
      children=[
          html.P("Test"),
          html.A("Aller vers test", href="/test"),
      ],
      style={"textAlign": "center", "backgroundColor": "#AAAAAA", "padding": "10px"},
  )