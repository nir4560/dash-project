import base64
import dash_html_components as html
from .contants import colors, color_a, color_c, boxStyle

with open("./src/assets/logo.jpg", "rb") as image_file:
    encoded_logo = base64.b64encode(image_file.read())

header = html.Header(children=[
    html.Img(src=f"data:image/jpg;base64,{encoded_logo.decode()}",
             style={
                 'height': '100%',
             }),
    html.H1(children='DS Dashboard',
            style={
                'margin': 0,
                'padding': '1em',
                'textAlign': 'center',
                'color': color_c,
            })
],
                     style={
                         "border": "1px solid white",
                         "margin": '0 0',
                         'align-items': 'center',
                         'backgroundColor': color_a,
                         "height": "10em",
                         "display": 'flex',
                         "borderRadius": " 0.5em",
                         "overflow": "hidden"
                     })
