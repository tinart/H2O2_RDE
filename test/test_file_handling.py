
import pytest
import os
import pandas as pd
from file_handling import ReadData
import shutil


@pytest.fixture
def setup_directory():
    path = "test_folder"
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, "test_file.csv"), "w") as f:
        f.write("col1,col2\n1,2\n3,4")
    yield path
    shutil.rmtree(path)


def test_init(setup_directory):
    read_data = ReadData(setup_directory)
    assert read_data.path == setup_directory


def test_create_new_folder(setup_directory):
    read_data = ReadData(setup_directory)
    read_data.create_new_folder()
    assert os.path.exists(os.path.join(setup_directory, "Analyzed"))


def test_count_files(setup_directory):
    read_data = ReadData(setup_directory)
    assert read_data.count_files() == 1


def test_get_filename(setup_directory):
    read_data = ReadData(setup_directory)
    assert read_data.get_filename() == "test_file.csv"


def test_read_data(setup_directory):
    read_data = ReadData(setup_directory)
    filename, df = read_data.read_data()
    assert isinstance(df, pd.DataFrame)

