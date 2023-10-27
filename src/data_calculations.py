from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

def fit_linear_regression(x, y):
    lr = LinearRegression()
    x = np.array(x).reshape(-1, 1)
    y = np.array(y).reshape(-1, 1)
    lr.fit(x, y)
    ypred = lr.predict(x)
    print("test syn")


    return lr.coef_, lr.intercept_, ypred

def baseline_regression(data, raw_data):
    return fit_linear_regression(data['Values']['x'], data['Values']['y'])

def baseline_correction_function(data, bsl_coefficient):
    corrected_current_value = data['WE(1).Current (A)'] - data['Time (s)'] * bsl_coefficient.item()
    corrected_dataframe = pd.DataFrame({'Time (s)': data['Time (s)'], 'Corrected Current (A)': corrected_current_value})
    return corrected_dataframe

def calibration_mean(data_selection):
    data = data_selection.copy()
    data['Concentration'] = pd.to_numeric(data['Concentration'])
    return data.groupby('Concentration', as_index=False).mean().rename(columns={'Concentration': 'Concentration Mean', 'Time': 'Time Mean', 'Signal': 'Signal Mean'})

def calibration_regression(data):
    calib_mean = calibration_mean(data)
    return fit_linear_regression(calib_mean['Concentration Mean'], calib_mean['Signal Mean'])

def signal_to_concentration(regression_parameters, truncated_data):
    a, b, _ = regression_parameters
    h2o2_y = (truncated_data['y'] - b) / a[0]

    return truncated_data['x'], h2o2_y

def initial_rate_regression(x,y):

    return fit_linear_regression(x, y)
