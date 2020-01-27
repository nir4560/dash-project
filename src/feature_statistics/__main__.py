import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import dash_table
import numpy as np
from ..contants import colors
from .common import true_ecdf, false_ecdf, false_interp, true_x_bar, true_y_bar
from .common import true_interp, false_interp, false_x_bar, false_y_bar
from .common import p_value, ks_statistic

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
                     style={'text-align': 'left'}),
        html.H3(id='chosen feature',
                children='Feature #1 Performance',
                style={'textAlign': 'center'}),
        html.Div(id='first graphs row',
                 style={'margin-bottom': '30px'},
                 className='row',
                 children=[
                     dcc.Graph(id='kde graph',
                               className='six columns',
                               figure={
                                   'data': [
                                       {
                                           'x': true_x_bar,
                                           'y': true_y_bar,
                                           'type': 'bar',
                                           'name': 'True Around GT'
                                       },
                                       {
                                           'x': false_x_bar,
                                           'y': false_y_bar,
                                           'type': 'bar',
                                           'name': 'False Around GT'
                                       },
                                   ],
                                   'layout': {
                                       'xaxis': {
                                           'title': 'Distance(m)'
                                       },
                                       'yaxis': {
                                           'title': 'Probability'
                                       },
                                       'plot_bgcolor': colors['background'],
                                       'paper_bgcolor': colors['background'],
                                       'title': 'Kernels Density Estimations',
                                       'font': {
                                           'color': colors['text']
                                       }
                                   }
                               }),
                     dcc.Graph(id='ecdf graph',
                               className='six columns',
                               figure={
                                   'data': [
                                       {
                                           'x': true_ecdf.x,
                                           'y': true_ecdf.y,
                                           'type': 'lines',
                                           'name': 'True Around GT'
                                       },
                                       {
                                           'x': false_ecdf.x,
                                           'y': false_ecdf.y,
                                           'type': 'lines',
                                           'name': 'False Around GT'
                                       },
                                   ],
                                   'layout': {
                                       'xaxis': {
                                           'title': 'Distance(m)'
                                       },
                                       'yaxis': {
                                           'title': 'Empirical CDF'
                                       },
                                       'plot_bgcolor': colors['background'],
                                       'paper_bgcolor': colors['background'],
                                       'title': 'ECDF Curves',
                                       'font': {
                                           'color': colors['text']
                                       }
                                   }
                               })
                 ]),
        html.Div(id='second graphs row',
                 className='row',
                 children=[
                     dcc.Graph(id='qq graph',
                               className='six columns',
                               figure={
                                   'data': [
                                       {
                                           'x': false_interp,
                                           'y': true_interp,
                                           'type': 'scatter',
                                           'name': 'True Around GT'
                                       },
                                       {
                                           'x': false_interp,
                                           'y': false_interp,
                                           'type': 'lines',
                                           'name': 'False Around GT'
                                       },
                                   ],
                                   'layout': {
                                       'xaxis': {
                                           'title': 'False Quantiles'
                                       },
                                       'yaxis': {
                                           'title': 'True Quantiles'
                                       },
                                       'plot_bgcolor': colors['background'],
                                       'paper_bgcolor': colors['background'],
                                       'title': 'Q-Q Plot',
                                       'font': {
                                           'color': colors['text']
                                       }
                                   }
                               })
                 ]),
        html.Div(
            id='tabular data, nulls pie and statistics',
            className="row",
            children=[
                html.Div(
                    id='tabular data',
                    style={'margin-top': '85px'},
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
                html.Div(
                    id='nulls pie',
                    className='four columns',
                    children=[
                        dcc.Graph(id='graph',
                                  figure=go.Figure([trace], layout))
                    ]),
                html.Div(
                    id='statistic tests',
                    style={'margin-top': '170px'},
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
                                   'text-align': 'center'
                               }),
                        html.P(
                            [
                                f"KS test pval: {p_value} ",
                                html.I("log"),
                                f"(pval): {np.log(p_value)} statistic: {ks_statistic}"
                            ],
                            style={
                                'border': '3px solid black',
                                'text-align': 'center',
                                'background-color': 'coral'
                            }),
                        html.P(
                            [
                                html.I("\u1D61"),
                                "\u00B2-test for NaNs pval: nan ",
                                html.I("log"), "(pval): nan statistic: 0.00"
                            ],
                            style={
                                'border': '3px solid black',
                                'text-align': 'center',
                                'background-color': 'MediumAquaMarine'
                            })
                    ])
            ])
    ])
