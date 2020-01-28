import dash_html_components as html
import dash_core_components as dcc
from ..contants import colors, boxStyle

# you can add as many charts as you like as long as you add the chartStyle to them
# if the number of charts is odd the last one will expand to fill the space
chartStyle = {
    **boxStyle,
    "min-width": "40%",
    "flex": "1",
}


kde_graph = lambda feature_data: dcc.Graph(id='kde graph',
                     style=chartStyle,
                     figure={
                         'data': [
                             {
                                 'x': feature_data['true_x_bar'],
                                 'y': feature_data['true_y_bar'],
                                 'type': 'bar',
                                 'name': 'True Around GT'
                             },
                             {
                                 'x': feature_data['false_x_bar'],
                                 'y': feature_data['false_y_bar'],
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
                     })


ecdf_graph = lambda feature_data : dcc.Graph(id='ecdf graph',
                     style=chartStyle,
                     figure={
                         'data': [
                             {
                                 'x': feature_data['true_ecdf'].x,
                                 'y': feature_data['true_ecdf'].y,
                                 'type': 'lines',
                                 'name': 'True Around GT'
                             },
                             {
                                 'x': feature_data['false_ecdf'].x,
                                 'y': feature_data['false_ecdf'].y,
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


qq_graph = lambda feature_data: dcc.Graph(
    id='qq graph',
    style=chartStyle,
    figure={
        'data': [
            {
                'x': feature_data['false_interp'],
                'y': feature_data['true_interp'],
                'type': 'scatter',
                'name': 'True Around GT'
            },
            {
                'x': feature_data['false_interp'],
                'y': feature_data['false_interp'],
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

graphsBox = lambda feature_data: html.Div(children=[
    kde_graph(feature_data),
    ecdf_graph(feature_data),
    qq_graph(feature_data)
],
                                          style={
                                              "display": "flex",
                                              "flex-flow": "wrap",
                                              "flex-wrap": "wrap",
                                              "margin": "-1em"
                                          })
