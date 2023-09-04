import pandas as pd
import pytest


import src.data_calculations

@pytest.fixture()
def baseline_test_data():
    data = {}
    data['Values'] = {'x':[0,1,2,3,4,5,6,7,8,9,10],'y':[0,2,4,6,8,10,12,14,16,18,20]}
    return data

def test_baseline_regression():
    pass