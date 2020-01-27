import dash_core_components as dcc
import dash_table
import dash_html_components as html
import plotly.graph_objects as go
from .statistic_tests import statistic_tests

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
    style={
        "background": "white",
        "padding": "1em"
    },
    children=[dcc.Graph(id='graph', figure=go.Figure([trace], layout))])

tabularData = html.Div(id='tabular data',
                       style={
                           'textAlign': 'center',
                           "marginBottom": "1em",
                       },
                       children=[
                           dash_table.DataTable(id='describe df',
                                                style_header={
                                                    'backgroundColor':
                                                    'rgb(30, 30, 30)',
                                                    'fontWeight': 'bold',
                                                },
                                                style_cell={
                                                    'backgroundColor':
                                                    'rgb(50, 50, 50)',
                                                    'color': 'white',
                                                })
                       ])

rightSide = html.Div(children=[tabularData, statistic_tests],
                     style={
                         "display": "flex",
                         "marginLeft": "1em",
                         "background": "white",
                         "padding": "1em",
                         "flexDirection": "column"
                     })

footer = html.Div(children=[nullsPie, rightSide],
                  style={
                      "display": "flex",
                      "marginTop": "2em",
                      "justifyContent": "center",
                      "alignItems": "flex-end"
                  })
