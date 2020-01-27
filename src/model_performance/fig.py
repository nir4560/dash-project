import plotly.graph_objects as go
from .common import calculated_confusion_matrix

fig = go.Figure(data=go.Heatmap(z=calculated_confusion_matrix,
                                x=['Morning', 'Afternoon', 'Evening'],
                                y=['Morning', 'Afternoon', 'Evening']),
                layout={
                    "yaxis": {
                        "autorange": "reversed"
                    },
                    "title": {
                        "text": "Confusion Matrix",
                        "x": 0.5
                    },
                    "yaxis_title": "True Mode",
                    "xaxis_title": "Predicted Mode"
                })
