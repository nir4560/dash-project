import dash_core_components as dcc
import dash_table
import dash_html_components as html
import plotly.graph_objects as go
from .statistic_tests import statistic_tests
from ..contants import boxStyle

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

nullsPie = html.Div(
    id='nulls pie',
    style=boxStyle,
    children=[dcc.Graph(id='graph', figure=go.Figure([trace], layout))])

tabularData = html.Div(id='tabular data',
                       style={
                           'textAlign': 'left',
                           "marginBottom": "1em",
                       },
                       children=[
                           dash_table.DataTable(id='describe df',
                                                style_header={
                                                    "textTransform":
                                                    "capitalize",
                                                    'backgroundColor': 'white',
                                                    'textAlign': "inherit",
                                                    'fontWeight': 'bold',
                                                    "paddingLeft": "2ch"
                                                },
                                                style_cell={
                                                    "paddingLeft": "2ch",
                                                    'backgroundColor': 'white',
                                                    'color': '#666',
                                                    'textAlign': "inherit"
                                                })
                       ])

rightSide = html.Div(children=[tabularData, statistic_tests],
                     style={
                         **boxStyle, "display": "flex",
                         "padding": "1em",
                         "flexDirection": "column"
                     })

footer = html.Div(children=[nullsPie, rightSide],
                  style={
                      "display": "flex",
                      "marginTop": "2em",
                      "justifyContent": "center",
                      "alignItems": "stretch"
                  })
