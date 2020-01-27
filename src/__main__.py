import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from .contants import color_a, color_b, color_c, color_d, color_e, colors
from .header import header
from .model_performance import model_performance
from .feature_statistics import feature_statistics
import plotly.graph_objects as go

describe_df = pd.DataFrame({
    'feature #1': [2, 4, 8, 0],
    'feature #2': [2, 0, 0, 0],
    'feature #3': [10, 2, 1, 8]
}).describe().reset_index()

# Kolmogorov - Smirnov - we want to reject the null hypothesis, i.e. reject the possibility that the two samples are
# coming from the exact same distribution.
# If the K-S statistic is small or the p-value is high, then we cannot reject the hypothesis that the distributions
#  of the two samples are the same.
# ------ not used anywhere!! ------

# dash visualization
external_stylesheets = [
    'https://codepen.io/chriddyp/pen/bWLwgP.css', "./assets/x.css"
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
    html.Div(id='main div', children=header),
    dcc.Tabs(id="tabs",
             value='tab-1',
             children=[
                 dcc.Tab(label='Feature Statistics', value='tab-1'),
                 dcc.Tab(label='Model Performance', value='tab-2'),
             ]),
    html.Div(id='tabs-content')
])


@app.callback(Output('tabs-content', 'children'), [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return feature_statistics
    elif tab == 'tab-2':
        return model_performance


@app.callback(output=Output(component_id='chosen feature',
                            component_property='children'),
              inputs=[
                  Input(component_id='select feature dropdown',
                        component_property='value')
              ])
def get_title_by_value(value):
    return f"{value} Performance"


@app.callback(output=[
    Output(component_id='describe df', component_property='columns'),
    Output(component_id='describe df', component_property='data')
],
              inputs=[
                  Input(component_id='select feature dropdown',
                        component_property='value')
              ])
def get_relevant_column(value):
    return [{
        "name": i,
        "id": i
    } for i in ['index', value.lower()]], describe_df[['index',
                                                       value.lower()
                                                       ]].to_dict('records')
