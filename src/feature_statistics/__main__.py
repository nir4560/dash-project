import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from ..app import app
from .graphs import graphsBox
from .footer import footer
from .common import getFeature

dropDown = dcc.Dropdown(id='select_feature_dropdown',
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
                        style={
                            'textAlign': 'left',
                            'marginBottom': '1em'
                        })

content_container = html.Div(id="feature_statistics_content",
                             style={"display": "static"})

feature_statistics = html.Div(id='main div',
                              children=[dropDown, content_container])


@app.callback(output=Output(component_id='feature_statistics_content',
                            component_property='children'),
              inputs=[
                  Input(component_id='select_feature_dropdown',
                        component_property='value')
              ])
def getContent(value):
    feature_data = getFeature(value)
    return [graphsBox(feature_data), footer(feature_data)]
