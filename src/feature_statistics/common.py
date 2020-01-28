from statsmodels.distributions.empirical_distribution import ECDF
from scipy.stats import ks_2samp
import pandas as pd

import numpy as np


# generate data
# replace with a method that returns data according to featureId
def getFeature(feature_id):
    print(f"i should replace this with actual data for feature {feature_id}")
    mu = 0
    sigma = 100
    false_around_gt = np.random.normal(mu, sigma, 100000)
    false_around_gt = abs(false_around_gt)
    true_around_gt = np.random.normal(mu, sigma / 10, 5000)
    true_around_gt = abs(true_around_gt)
    max_value = max(max(true_around_gt), max(false_around_gt))
    (true_y_bar, true_x_bar) = np.histogram(true_around_gt,
                                            bins=np.arange(max_value),
                                            density=True)
    (false_y_bar, false_x_bar) = np.histogram(false_around_gt,
                                              bins=np.arange(max_value),
                                              density=True)

    # fit an empirical ECDF
    false_ecdf = ECDF(false_around_gt)
    true_ecdf = ECDF(true_around_gt)
    true_ecdf.x[0] = false_ecdf.x[0] = 0
    if true_ecdf.x[-1] > false_ecdf.x[-1]:
        false_ecdf.x = np.concatenate(
            [false_ecdf.x, np.array([true_ecdf.x[-1]])])
        false_ecdf.y = np.concatenate(
            [false_ecdf.y, np.array([false_ecdf.y[-1]])])
    else:
        true_ecdf.x = np.concatenate(
            [true_ecdf.x, np.array([false_ecdf.x[-1]])])
        true_ecdf.y = np.concatenate(
            [true_ecdf.y, np.array([true_ecdf.y[-1]])])

    # qq plot
    if len(false_ecdf.x) > len(true_ecdf.x):
        # there are more false samples than true
        true_interp = np.interp(false_ecdf.x, true_ecdf.x, true_ecdf.y)
        false_interp = false_ecdf.y
    else:
        # there are more true samples than false
        false_interp = np.interp(true_ecdf.x, false_ecdf.x, false_ecdf.y)
        true_interp = true_ecdf.y

    ks_statistic, p_value = ks_2samp(false_around_gt, true_around_gt)
    return {
        "ks_statistic": ks_statistic,
        "p_value": p_value,
        "false_ecdf": false_ecdf,
        "true_ecdf": true_ecdf,
        "true_interp": true_interp,
        "false_interp": false_interp,
        "false_interp": false_interp,
        "true_interp": true_interp,
        "true_y_bar": true_y_bar,
        "true_x_bar": true_x_bar,
        "false_y_bar": false_y_bar,
        "false_x_bar": false_x_bar,
    }


describe_df = pd.DataFrame({
    'feature #1': [2, 4, 8, 0],
    'feature #2': [2, 0, 0, 0],
    'feature #3': [10, 2, 1, 8]
}).describe().reset_index()
