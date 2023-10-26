import pandas as pd
import os
import matplotlib.pyplot as plt
import shutil







class ReadData:

    def __init__(self, path:str):
        self.path = path
        self.file_list = []
        self.dictionary = {}
        self.data_cache = {}  # Cache to store read data for each file

    def create_new_folder(self)-> None:
        analyzed_directory = os.path.join(self.path, 'Analyzed')
        os.makedirs(analyzed_directory, exist_ok=True)

    def count_files(self):
        return sum(1 for file in os.listdir(self.path) if file.endswith(".csv"))

    def get_filename_list(self):
        self.file_list = [file for file in os.listdir(self.path) if file.endswith('.csv')]

    def read_data(self):
        for file in self.file_list:
            with open(os.path.join(self.path, file), 'r') as csv_file:
                self.data_cache[file] = pd.read_csv(csv_file, delimiter=',')

    def get_header(self, file) -> list:
        return list(self.data_cache[file].columns)

    def get_dataframe(self, file) -> pd.DataFrame:
        data = self.data_cache[file]
        col1, col2 = self.get_header(file)
        return pd.DataFrame({col1: data[col1], col2: data[col2]})

    def drop_nan_dataframe(self, file):
        df = self.get_dataframe(file)
        closest_index = (df['Time (s)'] - 2).abs().idxmin()
        return df.iloc[closest_index:].dropna()

    def create_data_dictionary(self, filename, analyzed_dataframe):
        self.dictionary[filename] = {'Time (s)': analyzed_dataframe['Time (s)'], '[H2O2]': analyzed_dataframe['[H2O2]']}

    def move_file_after_analysis(self, file):
        file_path = os.path.join(self.path, file)
        shutil.move(file_path, os.path.join(self.path, 'Analyzed'))