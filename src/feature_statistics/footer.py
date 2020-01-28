import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from .statistic_tests import statistic_tests
from ..contants import boxStyle
from .table import table

trace = go.Sunburst(
    ids=[
        "True", "False", "True Not Nan", "True Nan", "False Not Nan",
        "False Nan"
    ],
    labels=["True", "False", "Not Nan", "Nan", "Not Nan", "Nan"],
    parents=["All Samples", "All Samples", "True", "True", "False", "False"],
    values=[82, 18, 76, 6, 16, 2],
    outsidetextfont={
        "size": 20,
        "color": "#377eb8",
    },
    marker={"line": {
        "width": 2
    }},
)

layout = go.Layout(hovermode='closest',
                   margin=go.layout.Margin(t=50, l=0, r=0, b=0))

nullsPie = lambda feature_data: html.Div(
    id='nulls pie',
    style=boxStyle,
    children=[dcc.Graph(id='graph', figure=go.Figure([trace], layout))])

tabularData = lambda feature_data: html.Div(id='tabular data',
                                            style={
                                                "margin": "1em",
                                                "flex": "1",
                                                'textAlign': 'left',
                                            },
                                            children=[table])

rightSide = lambda feature_data: html.Div(
    children=[tabularData(feature_data),
              statistic_tests(feature_data)],
    style={
        **boxStyle, "display": "flex",
        "padding": "1em",
        "flexDirection": "column"
    })

footer = lambda feature_data: html.Div(children=[
    nullsPie(feature_data),
    tabularData(feature_data),
    statistic_tests(feature_data)
],
                                       style={
                                           "display": "flex",
                                           "marginTop": "2em",
                                           "justifyContent": "center",
                                           "alignItems": "stretch"
                                       })
