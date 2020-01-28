import dash_html_components as html
import numpy as np
from ..contants import boxStyle

basicStyle = {
    'border': '1px solid #666',
    'textAlign': 'center',
    "padding": "0.5em 2ch",
    "borderRadius": "0.5em"
}

statistical_significance = lambda feature_data: html.P([
    html.I("H0"), ": There is no statistical significance between samples.",
    html.Br(), "Color coded by ",
    html.I("\u03B1"), " = 0.05"
],
                                                       style=basicStyle)

ksTestPVal = lambda feature_data: html.P([
    f"KS test pval: {feature_data['p_value']} ",
    html.I("log"),
    f"(pval): {np.log(feature_data['p_value'])} statistic: {feature_data['ks_statistic']}"
],
                                         style={
                                             **basicStyle, 'backgroundColor':
                                             'coral'
                                         })

pVal = lambda feature_data: html.P([
    html.I("\u1D61"), "\u00B2-test for NaNs pval: nan ",
    html.I("log"), "(pval): nan statistic: 0.00"
],
                                   style={
                                       **basicStyle, 'backgroundColor':
                                       'MediumAquaMarine'
                                   })

statistic_tests = lambda feature_data: html.Div(id='statistic tests',
                                                style={
                                                    "margin": "1em",
                                                    "display": "flex",
                                                    'flexDirection': 'column',
                                                },
                                                children=[
                                                    statistical_significance(
                                                        feature_data),
                                                    ksTestPVal(feature_data),
                                                    pVal(feature_data)
                                                ])
