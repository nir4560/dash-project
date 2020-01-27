import dash_html_components as html
import dash_core_components as dcc
# the drop down and the title
dropDown = dcc.Dropdown(id='select feature dropdown',
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
                        style={'textAlign': 'left'})

title = html.H3(id='chosen feature',
                children='Feature #1 Performance',
                style={'textAlign': 'center'})

header = html.Div(children=[dropDown, title],
                  className="feature_statistics_header")
