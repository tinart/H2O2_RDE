import pandas as pd
import os
import matplotlib.pyplot as plt
import shutil
from datetime import datetime







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
        col1, col2, col3, col4 = self.get_header(file)
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

    def create_longform_dataframe(self,data_dictionary):
        # Create an empty DataFrame
        df = pd.DataFrame(columns=['Filename', 'Time (s)', '[H2O2]'])
        formated_date = datetime.now().strftime('%y%m%d')

        # Iterate through the dictionary and append 'a' and 'y' values as rows
        for filename, values in data_dictionary.items():
            if 'Time (s)' in values and '[H2O2]' in values:
                x_values = values['Time (s)']
                y_values = values['[H2O2]']
                temp_df = pd.DataFrame(
                    {'Filename': [filename] * len(x_values), 'Time (s)': x_values, '[H2O2]': y_values})
                df = pd.concat([df, temp_df], ignore_index=True)

        os.chdir(self.path)
        df.to_csv(f'{formated_date}_longform_analyzed_data.csv')

        return df