from statsmodels.distributions.empirical_distribution import ECDF
from scipy.stats import ks_2samp

import numpy as np

# generate data
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
    false_ecdf.x = np.concatenate([false_ecdf.x, np.array([true_ecdf.x[-1]])])
    false_ecdf.y = np.concatenate([false_ecdf.y, np.array([false_ecdf.y[-1]])])
else:
    true_ecdf.x = np.concatenate([true_ecdf.x, np.array([false_ecdf.x[-1]])])
    true_ecdf.y = np.concatenate([true_ecdf.y, np.array([true_ecdf.y[-1]])])

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
