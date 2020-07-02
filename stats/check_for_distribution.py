# a pseudo code for checking the distribution of a dataset acorss all of its attributes
# also report the goodness of fitment of any specific distribution to a data using "p-values"
# from Kolmogorov-Smirnov (KS) test
# author: Aman Singh (amansingh9097@gmai.com)

import pandas as pd
import numpy as np
import scipy
from sklearn.preprocessing import StandardScaler
import scipy.stats
# import warnings
# warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt


# change input file here
data = pd.read_csv('input_dataset.csv') 

# a quick look at the overall distribution of all numerical attributes
data.hist(bins=50, figsize=(20,15))
plt.show()

# trying different distributions and checking for their p-values
def get_distribution(data):
    size = len(data)
    
    # can add more distributions from here: https://docs.scipy.org/doc/scipy/reference/stats.html
    dist_names = ['norm', 'beta', 'lognorm', 'expon', 'pearson3', 'uniform', 'weibull_min', 'weibull_max']
    
    # reshaping for scaling & scaling for KS test
    sc = StandardScaler().fit(data.reshape(-1,1))
    
    dist_results = []
    for dist_name in dist_names:
        dist = getattr(scipy.stats, dist_name)
        param = dist.fit(data)
        pdf_fitted = dist.pdf(data, *param[:-2], loc=param[-2], scale=param[-1]) * size
        
        # applying KS-test (Kolmogorov-Smirnov)
        _, p = scipy.stats.kstest(sc.transform(data.reshape(-1,1)), dist_name, args=param)
        print('p-value for {} distribution = {}'.format(dist_name, p))
        dist_results.append((dist_name, p))
        
        plt.plot(pdf_fitted, label=dist_name)
        plt.xlim(0,52)
    plt.legend(loc='upper right')
    plt.show()
    
    # finding the best fitting distribution
    best_dist, best_p_val = (max(dist_results, key=lambda x: x[1]))
    print('Best fitting distribution: {} with p-value = {}'.format(best_dist, best_p_val))
    print()
    
# run the distribution assesment for all columns in pandas
for col in data.columns:
    print('-'*35)
    print('Fitting distributions across {}'.format(col))
    print('-'*35)
    
    get_distribution(data[col].values)
