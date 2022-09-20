import numpy as np
import pytest

from ReadFile import RDEdata
import pandas as pd


@pytest.fixture
def test_dataframe() -> pd.DataFrame:

    x = np.linspace(0, 50)
    y = np.linspace(100, 150)

    return pd.DataFrame({'x':x,'y':y})


def test_file_name(tmp_path):
    d = tmp_path / 'sub'
    d.mkdir()
    p = d / 'test.txt'
    p.write_text('Hello')


    test_data = RDEdata(path=d).file_name()
    assert test_data == 'test.txt'

def test_read_file():

    pass








