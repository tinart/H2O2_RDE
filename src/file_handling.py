import pandas as pd
import os
import matplotlib.pyplot as plt
import shutil






class ReadData:

    def __init__(self, path:str):
        self.path = path
        self.file = []
        self.dictionary = {}
        self.data_cache = None  # Cache to store read data

    def create_new_folder(self)-> None:
        analyzed_directory = os.path.join(self.path, 'Analyzed')
        os.makedirs(analyzed_directory, exist_ok=True)

    def count_files(self):
        csv_file_count = sum(1 for file in os.listdir(self.path) if file.endswith(".csv"))
        return csv_file_count

    def get_filename(self):
        for file in os.listdir(self.path):
            if file.endswith('.csv'):
                return file

    def read_data(self) -> pd.DataFrame:
        if self.data_cache is None:
            for file in os.listdir(self.path):
                if file.endswith('.csv'):
                    self.file.append(file)
                    with open(os.path.join(self.path, file), 'r') as rde_txtfile:
                        self.data_cache = pd.read_csv(rde_txtfile, delimiter=',')
        return self.file[-1], self.data_cache

    def get_header(self) -> list:
        _, data = self.read_data()
        return list(data.columns)

    def get_dataframe(self) -> pd.DataFrame:
        _, data = self.read_data()
        col1, col2, col3, col4 = self.get_header()
        return pd.DataFrame({col1: data[col1], col2: data[col2]})

    def drop_nan_dataframe(self):
        df = self.get_dataframe()
        closest_index = (df['Time (s)'] - 2).abs().idxmin()
        truncated_dataframe = df.iloc[closest_index:].dropna()
        return truncated_dataframe

    def create_data_dictionary(self, filename, analyzed_dataframe):
        self.dictionary[filename] = {'Time (s)': analyzed_dataframe[0], '[H2O2]': analyzed_dataframe[1]}
        return self.dictionary

    def move_file_after_analysis(self):
        try:
            file, _ = self.read_data()
            file_path = os.path.join(self.path, file)
            shutil.move(file_path, os.path.join(self.path, 'Analyzed'))
        except Exception as e:
            print(f"Error while moving file: {e}")