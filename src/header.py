import base64
import dash_html_components as html
from .contants import colors

with open("./assets/logo.jpg", "rb") as image_file:
    encoded_logo = base64.b64encode(image_file.read())

header = [
    html.Img(src=f"data:image/jpg;base64,{encoded_logo.decode()}",
             style={
                 'height': '70px',
                 'position': 'absolute',
                 'left': '10px',
                 'top': '10px'
             }),
    html.H1(children='DS Dashboard',
            style={
                'margin': 0,
                'padding': '10px',
                'backgroundColor': colors['background'],
                'textAlign': 'center',
                'color': colors['text']
            })
]
