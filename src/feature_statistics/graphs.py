import dash_core_components as dcc
from .common import true_ecdf, false_ecdf, false_interp, true_x_bar, true_y_bar
from .common import true_interp, false_interp, false_x_bar, false_y_bar
from ..contants import colors

kde_graph = dcc.Graph(id='kde graph',
                      className='six columns',
                      figure={
                          'data': [
                              {
                                  'x': true_x_bar,
                                  'y': true_y_bar,
                                  'type': 'bar',
                                  'name': 'True Around GT'
                              },
                              {
                                  'x': false_x_bar,
                                  'y': false_y_bar,
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

ecdf_graph = dcc.Graph(id='ecdf graph',
                       className='six columns',
                       figure={
                           'data': [
                               {
                                   'x': true_ecdf.x,
                                   'y': true_ecdf.y,
                                   'type': 'lines',
                                   'name': 'True Around GT'
                               },
                               {
                                   'x': false_ecdf.x,
                                   'y': false_ecdf.y,
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

qq_graph = dcc.Graph(id='qq graph',
                     className='six columns',
                     figure={
                         'data': [
                             {
                                 'x': false_interp,
                                 'y': true_interp,
                                 'type': 'scatter',
                                 'name': 'True Around GT'
                             },
                             {
                                 'x': false_interp,
                                 'y': false_interp,
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
