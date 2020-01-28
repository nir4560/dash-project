import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from .contants import color_a, color_b, color_c, color_d, color_e, colors
from .header import header
from .model_performance import model_performance
from .feature_statistics import feature_statistics
import plotly.graph_objects as go
from .app import app

# Kolmogorov - Smirnov - we want to reject the null hypothesis, i.e. reject the possibility that the two samples are
# coming from the exact same distribution.
# If the K-S statistic is small or the p-value is high, then we cannot reject the hypothesis that the distributions
#  of the two samples are the same.
# ------ not used anywhere!! ------

app.layout = html.Div([
    html.Div(id='main div', children=header),
    dcc.Tabs(id="tabs",
             style={
                 "margin": "1em 0",
             },
             value='featureStatistics',
             children=[
                 dcc.Tab(label='Feature Statistics',
                         value='featureStatistics'),
                 dcc.Tab(label='Model Performance', value='modelPerformance'),
             ]),
    html.Div(id='tabs-content')
],
                      style={"padding": "1em"})


@app.callback(Output('tabs-content', 'children'), [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'featureStatistics':
        return feature_statistics
    elif tab == 'modelPerformance':
        return model_performance

