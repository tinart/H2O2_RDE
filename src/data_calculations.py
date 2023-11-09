from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np

def fit_linear_regression(x, y):
    lr = LinearRegression()
    x = np.array(x).reshape(-1, 1)
    y = np.array(y).reshape(-1, 1)
    lr.fit(x, y)
    ypred = lr.predict(x)



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


def rolling_regression(group, window_size=15):
    # Convert to numpy arrays for faster computation
    time_values = group['Time (s)'].values
    concentration_values = group['[H2O2]'].values
    time_diffs = np.cumsum(np.ediff1d(time_values, to_begin=0))

    # Initialize variables to store the steepest slope, intercept and the corresponding window
    steepest_slope = None
    steepest_intercept = None
    steepest_window = (None, None)

    # Iterate over the time series data to perform rolling regression
    for start in range(len(time_values)):
        end = start
        while end < len(time_values) and time_diffs[end] - time_diffs[start] < window_size:
            end += 1
        if end - start > 1:
            X = time_values[start:end].reshape(-1, 1)
            y = concentration_values[start:end]
            model = LinearRegression()
            model.fit(X, y)
            slope = model.coef_[0]
            intercept = model.intercept_
            if steepest_slope is None or (slope < steepest_slope and slope < 0):
                steepest_slope = slope
                steepest_intercept = intercept
                steepest_window = (time_values[start], time_values[end - 1])
        start = end - 1

    return steepest_slope, steepest_intercept, steepest_window


