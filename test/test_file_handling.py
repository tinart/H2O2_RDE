import os.path
import unittest
import pandas as pd
from file_handling import ReadData
import pytest
from src.file_handling import ReadData

@pytest.fixture
def sample_data(tmpdir):
    csv_file = tmpdir.join("sample.csv")
    csv_file.write("Time (s),WE(1).Current (A),Corrected Time (s),Index\n1,0.1,1.1,1\n2,0.2,2.1,2\n3,0.3,3.1,3\n")
    return csv_file

def test_read_data(sample_data):
    data_reader = ReadData(sample_data.dirname)
    data = data_reader.read_data()
    assert isinstance(data, pd.DataFrame)
    assert len(data) == 3
    assert 'Time (s)' in data.columns
    assert 'WE(1).Current (A)' in data.columns


def test_get_header(sample_data):
    data_reader = ReadData(sample_data.dirname)
    data = data_reader.get_header()
    assert isinstance(data, list)

def test_get_dataframe(sample_data):
    data_reader = ReadData(sample_data.dirname)
    data = data_reader.get_dataframe()
    assert isinstance(data, pd.DataFrame)

def test_create_new_folder(sample_data):
    data_reader = ReadData(sample_data.dirname)
    data_reader.create_new_folder()

    assert os.path.exists(sample_data.dirname)


def test_drop_nan_dataframe(sample_data):
    data_reader = ReadData(sample_data.dirname)
    data = data_reader.drop_nan_dataframe()
    assert isinstance(data, pd.DataFrame)
    assert len(data) == 2
    assert 'Time (s)' in data.columns
    assert 'WE(1).Current (A)' in data.columns

# Add more tests for other methods

if __name__ == '__main__':
    pytest.main()