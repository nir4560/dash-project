import dash_html_components as html
import dash_core_components as dcc
from .feature_importance_graphs import feature_importance_graphs
from .fig import fig

model_performance = html.Div(
    id='main div',
    children=[
        html.Div(id='confusion matrix div',
                 className='row',
                 children=[dcc.Graph(id='price_volume', figure=fig)]),
        html.Div(id='feature importance first div',
                 className='row',
                 children=feature_importance_graphs[0:3]),
        html.Div(id='feature importance second div',
                 className='row',
                 children=feature_importance_graphs[3:])
    ])
