# from pypfopt import EfficientFrontier
# from pypfopt import risk_models
# from pypfopt import expected_returns

import pandas as pd
import numpy as np
from collections import Counter

# # data
# futures_raw_data_file = r'C:\Users\Dell\Documents\SynologyDrive\实习\国君自营\工作\期货策略\20221001-顾高臣\multi_asset.csv'
# futures_raw_data = pd.read_csv(futures_raw_data_file)
# futures_raw_data.set_index('Date', drop=True, inplace=True)
# benchmark_SP500 = futures_raw_data['benchmark_SP500']
# df = futures_raw_data.iloc[:, 1:]


# # mvo
# # Calculate expected returns and sample covariance
# mu = expected_returns.mean_historical_return(df)
# S = risk_models.sample_cov(df)

# # Optimize for maximal Sharpe ratio
# ef = EfficientFrontier(mu, S, weight_bounds=(-1, 1))
# raw_weights = ef.max_sharpe()
# cleaned_weights = ef.clean_weights()

# print(cleaned_weights)


a = np.array([1,1,2,3])
print(Counter(a)[1])



    