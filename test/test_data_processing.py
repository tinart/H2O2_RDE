
import pytest
import pandas as pd
from data_processing import RawPlot, BaseLineCorrection

@pytest.fixture
def setup_dataframe():
    df = pd.DataFrame({'Time': [1, 2, 3], 'Value': [0.1, 0.2, 0.3]})
    return df

def test_RawPlot_init(setup_dataframe):
    raw_plot = RawPlot(setup_dataframe)
    assert isinstance(raw_plot.df, pd.DataFrame)

def test_RawPlot_get_colnames(setup_dataframe):
    raw_plot = RawPlot(setup_dataframe)
    assert raw_plot.get_colnames == ['Time', 'Value']

def test_BaseLineCorrection_init(setup_dataframe):
    baseline_correction = BaseLineCorrection(setup_dataframe)
    assert isinstance(baseline_correction.df, pd.DataFrame)

def test_BaseLineCorrection_get_colnames(setup_dataframe):
    baseline_correction = BaseLineCorrection(setup_dataframe)
    assert baseline_correction.get_colnames == ['Time', 'Value']