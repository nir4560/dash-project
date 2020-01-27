from statsmodels.distributions.empirical_distribution import ECDF
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import dash_table
import base64
import pickle
from sklearn.metrics import confusion_matrix
from sklearn import datasets
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
import plotly.graph_objects as go
from scipy.stats import ks_2samp


# generate data
mu = 0
sigma = 100
false_around_gt = np.random.normal(mu, sigma, 100000)
false_around_gt = abs(false_around_gt)
true_around_gt = np.random.normal(mu, sigma / 10, 5000)
true_around_gt = abs(true_around_gt)
max_value = max(max(true_around_gt), max(false_around_gt))
(true_y_bar, true_x_bar) = np.histogram(true_around_gt, bins=np.arange(max_value), density=True)
(false_y_bar, false_x_bar) = np.histogram(false_around_gt, bins=np.arange(max_value), density=True)

describe_df = pd.DataFrame({'feature #1': [2, 4, 8, 0],
                            'feature #2': [2, 0, 0, 0],
                            'feature #3': [10, 2, 1, 8]}).describe().reset_index()

# Kolmogorov - Smirnov - we want to reject the null hypothesis, i.e. reject the possibility that the two samples are
# coming from the exact same distribution.
# If the K-S statistic is small or the p-value is high, then we cannot reject the hypothesis that the distributions
#  of the two samples are the same.
ks_statistic, p_value = ks_2samp(false_around_gt, true_around_gt)

# fit an empirical ECDF
false_ecdf = ECDF(false_around_gt)
true_ecdf = ECDF(true_around_gt)
true_ecdf.x[0] = false_ecdf.x[0] = 0
if true_ecdf.x[-1] > false_ecdf.x[-1]:
    false_ecdf.x = np.concatenate([false_ecdf.x, np.array([true_ecdf.x[-1]])])
    false_ecdf.y = np.concatenate([false_ecdf.y, np.array([false_ecdf.y[-1]])])
else:
    true_ecdf.x = np.concatenate([true_ecdf.x, np.array([false_ecdf.x[-1]])])
    true_ecdf.y = np.concatenate([true_ecdf.y, np.array([true_ecdf.y[-1]])])

# qq plot
if len(false_ecdf.x) > len(true_ecdf.x):
    # there are more false samples than true
    true_interp = np.interp(false_ecdf.x, true_ecdf.x, true_ecdf.y)
    false_interp = false_ecdf.y
else:
    # there are more true samples than false
    false_interp = np.interp(true_ecdf.x, false_ecdf.x, false_ecdf.y)
    true_interp = true_ecdf.y

# dash visualization
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

with open("logo.jpg", "rb") as image_file:
    encoded_logo = base64.b64encode(image_file.read())

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config['suppress_callback_exceptions'] = True

colors = {
    'background': '#f9f9f9',
    'text': '#7FDBFF'
}

app.layout = html.Div([
    html.Div(id='main div', children=[
        html.Img(src=f"data:image/jpg;base64,{encoded_logo.decode()}",
                 style={'height': '70px', 'position': 'absolute', 'left': '10px', 'top': '10px'})
        ,
        html.H1(
            children='DS Dashboard',
            style={
                'margin': 0,
                'padding': '10px',
                'background-color': colors['background'],
                'textAlign': 'center',
                'color': colors['text']
            }
        )]),
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Feature Statistics', value='tab-1'),
        dcc.Tab(label='Model Performance', value='tab-2'),
    ]),
    html.Div(id='tabs-content')
])


@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return first_layout
    elif tab == 'tab-2':
        return second_layout


trace = go.Sunburst(
    ids=["True", "False", "True Not Nan", "True Nan", "False Not Nan", "False Nan"],
    labels=["True", "False", "Not Nan", "Nan", "Not Nan", "Nan"],
    parents=["All Samples", "All Samples", "True", "True", "False", "False"],
    values=[82, 18, 76, 6, 16, 2],
    outsidetextfont={"size": 20, "color": "#377eb8"},
    marker={"line": {"width": 2}},
)
layout = go.Layout(hovermode='closest'
                   , margin=go.layout.Margin(t=50, l=0, r=0, b=0)
                   )

first_layout = html.Div(id='main div', children=[
    dcc.Dropdown(id='select feature dropdown',
                 options=[
                     {'label': 'Feature #1', 'value': 'Feature #1'},
                     {'label': 'Feature #2', 'value': 'Feature #2'},
                     {'label': 'Feature #3', 'value': 'Feature #3'}
                 ],
                 value='Feature #1',
                 style={'text-align': 'left'}
                 ),
    html.H3(id='chosen feature', children='Feature #1 Performance', style={
        'textAlign': 'center'
    }),
    html.Div(id='first graphs row', style={'margin-bottom': '30px'}, className='row', children=[
        dcc.Graph(
            id='kde graph',
            className='six columns',
            figure={
                'data': [
                    {'x': true_x_bar, 'y': true_y_bar,
                     'type': 'bar', 'name': 'True Around GT'},
                    {'x': false_x_bar, 'y': false_y_bar, 'type': 'bar',
                     'name': 'False Around GT'},
                ],
                'layout': {
                    'xaxis': {'title': 'Distance(m)'},
                    'yaxis': {'title': 'Probability'},
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'title': 'Kernels Density Estimations',
                    'font': {
                        'color': colors['text']
                    }
                }
            }
        )
        ,
        dcc.Graph(
            id='ecdf graph',
            className='six columns',
            figure={
                'data': [
                    {'x': true_ecdf.x, 'y': true_ecdf.y,
                     'type': 'lines', 'name': 'True Around GT'},
                    {'x': false_ecdf.x, 'y': false_ecdf.y, 'type': 'lines',
                     'name': 'False Around GT'},
                ],
                'layout': {
                    'xaxis': {'title': 'Distance(m)'},
                    'yaxis': {'title': 'Empirical CDF'},
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'title': 'ECDF Curves',
                    'font': {
                        'color': colors['text']
                    }
                }
            }
        )])
    ,
    html.Div(id='second graphs row', className='row', children=[
        dcc.Graph(
            id='qq graph',
            className='six columns',
            figure={
                'data': [
                    {'x': false_interp, 'y': true_interp,
                     'type': 'scatter', 'name': 'True Around GT'},
                    {'x': false_interp, 'y': false_interp, 'type': 'lines',
                     'name': 'False Around GT'},
                ],
                'layout': {
                    'xaxis': {'title': 'False Quantiles'},
                    'yaxis': {'title': 'True Quantiles'},
                    'plot_bgcolor': colors['background'],
                    'paper_bgcolor': colors['background'],
                    'title': 'Q-Q Plot',
                    'font': {
                        'color': colors['text']
                    }
                }
            }
        )])
    ,
    html.Div(id='tabular data, nulls pie and statistics', className="row",
             children=[
                 html.Div(id='tabular data', style={'margin-top': '85px'},
                          className='four columns', children=[
                         dash_table.DataTable(
                             id='describe df',
                             style_header={
                                 'backgroundColor': 'rgb(30, 30, 30)',
                                 'fontWeight': 'bold',
                                 'textAlign': 'center'
                             },
                             style_cell={
                                 'backgroundColor': 'rgb(50, 50, 50)',
                                 'color': 'white',
                                 'textAlign': 'center'
                             }
                         )]),
                 html.Div(id='nulls pie', className='four columns',
                          children=[
                              dcc.Graph(
                                  id='graph',
                                  figure=go.Figure([trace], layout)
                              )]),
                 html.Div(id='statistic tests', style={'margin-top': '170px'},
                          className='four columns',
                          children=[
                              html.P(
                                  [html.I("H0"), ": There is no statistical significance between samples.", html.Br(),
                                   "Color coded by ", html.I("\u03B1"), " = 0.05"],
                                  style={'border': '3px solid black', 'text-align': 'center'}),
                              html.P([f"KS test pval: {p_value} ", html.I("log"),
                                      f"(pval): {np.log(p_value)} statistic: {ks_statistic}"],
                                     style={'border': '3px solid black', 'text-align': 'center',
                                            'background-color': 'coral'}),
                              html.P(
                                  [html.I("\u1D61"), "\u00B2-test for NaNs pval: nan ", html.I("log"),
                                   "(pval): nan statistic: 0.00"],
                                  style={'border': '3px solid black', 'text-align': 'center',
                                         'background-color': 'MediumAquaMarine'})
                          ])
             ])
])


@app.callback(output=Output(component_id='chosen feature', component_property='children'),
              inputs=[Input(component_id='select feature dropdown', component_property='value')])
def get_title_by_value(value):
    return f"{value} Performance"


@app.callback(output=[Output(component_id='describe df', component_property='columns'),
                      Output(component_id='describe df', component_property='data')],
              inputs=[Input(component_id='select feature dropdown', component_property='value')])
def get_relevant_column(value):
    return [{"name": i, "id": i} for i in ['index', value.lower()]], describe_df[
        ['index', value.lower()]].to_dict(
        'records')


iris = datasets.load_iris()
X = iris.data
y = iris.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
bst = XGBClassifier(max_depth=1, silent=True, objective='multi:softprob')
bst.fit(X_train, y_train)
preds = bst.predict(X_test)
with open("model.txt", "rb") as f:
    model = pickle.loads(f.read())
confusion_matrix = confusion_matrix(y_test, preds)

feature_importance_graphs = list()
for importance_type in ['weight', 'gain', 'cover', 'total_gain', 'total_cover']:
    curr_importances = bst.get_booster().get_score(importance_type=importance_type)
    curr_importances = {k: v for k, v in sorted(curr_importances.items(), key=lambda item: item[1])}
    feature_importance_graphs.extend([dcc.Graph(
        id=f'{importance_type} graph',
        className='four columns',
        figure={
            'data': [
                {'y': list(curr_importances.keys()), 'x': list(curr_importances.values()),
                 'type': 'bar', 'name': f'{importance_type} feature importance', 'orientation': 'h'},
            ],
            'layout': {
                'title': importance_type,
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }
            }
        })])

fig = go.Figure(data=go.Heatmap(z=confusion_matrix, x=['Morning', 'Afternoon', 'Evening'],
                                y=['Morning', 'Afternoon', 'Evening']),
                layout={"yaxis": {"autorange": "reversed"},
                        "title": {"text": "Confusion Matrix", "x": 0.5},
                        "yaxis_title": "True Mode",
                        "xaxis_title": "Predicted Mode"})

second_layout = html.Div(id='main div',
                         children=[html.Div(id='confusion matrix div', className='row', children=[
                             dcc.Graph(id='price_volume', figure=fig)]),
                                   html.Div(id='feature importance first div', className='row',
                                            children=feature_importance_graphs[0:3]),
                                   html.Div(id='feature importance second div', className='row',
                                            children=feature_importance_graphs[3:])])

if __name__ == '__main__':
    app.run_server(debug=True)
