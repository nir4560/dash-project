import dash_html_components as html
from .graphs import graphsBox
from .footer import footer
from .header import header

feature_statistics = html.Div(id='main div',
                              children=[header, graphsBox, footer])
