

import src.data_calculations


import pytest
import numpy as np
import pandas as pd
from src.data_calculations import (fit_linear_regression, baseline_regression, baseline_correction_function,
                                   calibration_mean, v_to_tn)


def setup_dataframe():
    df = pd.DataFrame({'Time': [1, 2, 3], 'Coefficient': [0.1, 0.2, 0.3]})
    return df

def check_column_exists(df, column_name):
    return column_name in df.columns


    df = pd.DataFrame()
def test_fit_linear_regression():
    x = [1, 2, 3, 4, 5]
    y = [2, 4, 3, 4, 5]
    coef, intercept, ypred = fit_linear_regression(x, y)
    assert isinstance(coef, np.ndarray)
    assert isinstance(intercept, np.ndarray)
    assert isinstance(ypred, np.ndarray)


def test_baseline_regression():
    data = {'Values': {'x': [1, 2, 3, 4, 5], 'y': [2, 4, 3, 4, 5]}}
    coef, intercept, ypred = baseline_regression(data, None)
    assert isinstance(coef, np.ndarray)
    assert isinstance(intercept, np.ndarray)
    assert isinstance(ypred, np.ndarray)


def test_baseline_correction_function():
    data = pd.DataFrame({'Time (s)': [1, 2, 3], 'WE(1).Current (A)': [0.1, 0.2, 0.3]})
    bsl_coefficient = np.array([0.01])
    corrected_df = baseline_correction_function(data, bsl_coefficient)
    assert isinstance(corrected_df, pd.DataFrame)


def test_calibration_mean():
    data = pd.DataFrame({'Concentration': ['1', '1', '2', '2'], 'Current': [0.1, 0.2, 0.3, 0.4]})
    mean_df = calibration_mean(data)
    assert isinstance(mean_df, pd.DataFrame)

def test_v_to_tn():
    data = setup_dataframe()
    enzyme_c = 1

    df = v_to_tn(data,enzyme_c)

    assert isinstance(data, pd.DataFrame)
    assert isinstance(df, pd.DataFrame)
    assert check_column_exists(df,'Turnover_Number')
