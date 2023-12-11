import pandas as pd
import os
import shutil
from datetime import datetime
import time

def time_function(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {func.__name__} took {end_time - start_time} seconds to complete.")
        return result
    return wrapper




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


def find_csv_files(path):
    """
    Search the current directory for CSV files and list them as options for the user to select.

    Returns:
        A list of CSV file paths in the current directory.
    """
    csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
    return csv_files

def select_csv_file(csv_files, path):
    """
    Prompt the user to select a CSV file from a list of files.

    Parameters:
        csv_files: A list of CSV file names.

    Returns:
        The path of the selected CSV file.
    """
    print("Please select a CSV file to proceed:")
    for idx, file in enumerate(csv_files):
        print(f"{idx + 1}. {file}")

    while True:
        try:
            selection = int(input("Enter the number of the CSV file you want to select: "))
            # Adjust for zero-based index
            if 1 <= selection <= len(csv_files):
                return os.path.join(path,csv_files[selection - 1])
            else:
                print("Invalid selection. Please try again.")
                break
        except ValueError:
            print("Invalid input. Please enter a number.")


def ask_for_enzyme_concentration():

    try:
        enzyme_c = float(input('Enter the enzyme concentration used in this experiment'))
        return enzyme_c
    except ValueError:
        print('Invalid input, please enter a number.')
