from dash import html

def get_header():
  """Returns the footer component."""
  return html.Header(
      id="header",
      children=[
          html.P("HEADER"),
      ],
      style={"textAlign": "center", "backgroundColor": "#AAAAAA", "padding": "10px"},
  )