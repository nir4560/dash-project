import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import dash_table
import numpy as np
from ..contants import colors
from .common import p_value, ks_statistic
from .graphs import qq_graph, kde_graph, ecdf_graph

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
        "color": "#377eb8"
    },
    marker={"line": {
        "width": 2
    }},
)

layout = go.Layout(hovermode='closest',
                   margin=go.layout.Margin(t=50, l=0, r=0, b=0))

feature_statistics = html.Div(
    id='main div',
    children=[
        dcc.Dropdown(id='select feature dropdown',
                     options=[{
                         'label': 'Feature #1',
                         'value': 'Feature #1'
                     }, {
                         'label': 'Feature #2',
                         'value': 'Feature #2'
                     }, {
                         'label': 'Feature #3',
                         'value': 'Feature #3'
                     }],
                     value='Feature #1',
                     style={'textAlign': 'left'}),
        html.H3(id='chosen feature',
                children='Feature #1 Performance',
                style={'textAlign': 'center'}),
        html.Div(id='first graphs row',
                 style={'marginBottom': '30px'},
                 className='row',
                 children=[kde_graph, ecdf_graph]),
        html.Div(id='second graphs row', className='row', children=[qq_graph]),
        html.Div(
            id='tabular data, nulls pie and statistics',
            className="row",
            children=[
                html.Div(id='tabular data',
                         style={'marginTop': '85px'},
                         className='four columns',
                         children=[
                             dash_table.DataTable(id='describe df',
                                                  style_header={
                                                      'backgroundColor':
                                                      'rgb(30, 30, 30)',
                                                      'fontWeight': 'bold',
                                                      'textAlign': 'center'
                                                  },
                                                  style_cell={
                                                      'backgroundColor':
                                                      'rgb(50, 50, 50)',
                                                      'color': 'white',
                                                      'textAlign': 'center'
                                                  })
                         ]),
                html.Div(id='nulls pie',
                         className='four columns',
                         children=[
                             dcc.Graph(id='graph',
                                       figure=go.Figure([trace], layout))
                         ]),
                html.Div(
                    id='statistic tests',
                    style={'marginTop': '170px'},
                    className='four columns',
                    children=[
                        html.P([
                            html.I("H0"),
                            ": There is no statistical significance between samples.",
                            html.Br(), "Color coded by ",
                            html.I("\u03B1"), " = 0.05"
                        ],
                               style={
                                   'border': '3px solid black',
                                   'textAlign': 'center'
                               }),
                        html.P(
                            [
                                f"KS test pval: {p_value} ",
                                html.I("log"),
                                f"(pval): {np.log(p_value)} statistic: {ks_statistic}"
                            ],
                            style={
                                'border': '3px solid black',
                                'textAlign': 'center',
                                'backgroundColor': 'coral'
                            }),
                        html.P(
                            [
                                html.I("\u1D61"),
                                "\u00B2-test for NaNs pval: nan ",
                                html.I("log"), "(pval): nan statistic: 0.00"
                            ],
                            style={
                                'border': '3px solid black',
                                'textAlign': 'center',
                                'backgroundColor': 'MediumAquaMarine'
                            })
                    ])
            ])
    ])
