import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import dash_table
from sklearn import datasets
from sklearn.model_selection import train_test_split
from scipy.stats import ks_2samp
from .contants import color_a, color_b, color_c, color_d, color_e, colors
from .header import header
from .feature_statistics import layout as feature_statistics
from .model_performance import layout as model_performance
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
ks_statistic, p_value = ks_2samp(false_around_gt, true_around_gt)

# dash visualization
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

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


iris = datasets.load_iris()
X = iris.data
y = iris.target
X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.2,
                                                    random_state=42)
