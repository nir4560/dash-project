import dash_table
from dash.dependencies import Input, Output
from .common import describe_df
from ..app import app

table = dash_table.DataTable(id='describe_df',
                             style_header={
                                 "textTransform": "capitalize",
                                 'textAlign': "inherit",
                                 'fontWeight': 'bold',
                                 "paddingLeft": "2ch",
                             },
                             style_cell={
                                 "background": "transparent",
                                 "paddingLeft": "2ch",
                                 'textAlign': "inherit"
                             })


@app.callback(output=[
    Output(component_id='describe_df', component_property='columns'),
    Output(component_id='describe_df', component_property='data')
],
              inputs=[
                  Input(component_id='select_feature_dropdown',
                        component_property='value')
              ])
def setup_table_columns(value):
    return [{
        "name": i,
        "id": i
    } for i in ['index', value.lower()]], describe_df[['index',
                                                       value.lower()
                                                       ]].to_dict('records')
