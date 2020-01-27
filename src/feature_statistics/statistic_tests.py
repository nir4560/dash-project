import dash_html_components as html
import numpy as np
from .common import p_value, ks_statistic

basicStyle = {'border': '3px solid black', 'textAlign': 'center'}

statistical_significance = html.P([
    html.I("H0"), ": There is no statistical significance between samples.",
    html.Br(), "Color coded by ",
    html.I("\u03B1"), " = 0.05"
],
                                  style=basicStyle)

ksTestPVal = html.P([
    f"KS test pval: {p_value} ",
    html.I("log"), f"(pval): {np.log(p_value)} statistic: {ks_statistic}"
],
                    style={
                        **basicStyle, 'backgroundColor': 'coral'
                    })
pVal = html.P([
    html.I("\u1D61"), "\u00B2-test for NaNs pval: nan ",
    html.I("log"), "(pval): nan statistic: 0.00"
],
              style={
                  **basicStyle, 'backgroundColor': 'MediumAquaMarine'
              })

statistic_tests = html.Div(
    id='statistic tests',
    style={
        "display": "flex",
        'flexDirection': 'column',
    },
    children=[statistical_significance, ksTestPVal, pVal])
