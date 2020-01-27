import dash_core_components as dcc
from .common import bst
from ..contants import colors

importance_types = ['weight', 'gain', 'cover', 'total_gain', 'total_cover']

feature_importance_graphs = list()
for importance_type in importance_types:
    curr_importances = bst.get_booster().get_score(
        importance_type=importance_type)
    curr_importances = {
        k: v
        for k, v in sorted(curr_importances.items(), key=lambda item: item[1])
    }
    feature_importance_graphs.extend([
        dcc.Graph(id=f'{importance_type} graph',
                  className='four columns',
                  figure={
                      'data': [
                          {
                              'y': list(curr_importances.keys()),
                              'x': list(curr_importances.values()),
                              'type': 'bar',
                              'name': f'{importance_type} feature importance',
                              'orientation': 'h'
                          },
                      ],
                      'layout': {
                          'title': importance_type,
                          'plot_bgcolor': colors['background'],
                          'paper_bgcolor': colors['background'],
                          'font': {
                              'color': colors['text']
                          }
                      }
                  })
    ])
