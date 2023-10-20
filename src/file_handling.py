
import pandas as pd
import os
import matplotlib.pyplot as plt
import shutil

class ReadData:

    def __init__(self, path:str):

        self.path = path
        self.file = []
        self.dictionary = {}


    def create_new_folder(self)-> None:

        analyzed_directory = os.path.join(self.path, 'Analyzed')
        os.makedirs(analyzed_directory, exist_ok=True)
    def count_files(self):
        csv_file_count = sum(1 for file in os.listdir(self.path) if file.endswith(".csv"))
        return csv_file_count

    def get_filename(self):

        for file in os.listdir(self.path):




            if file.endswith('.csv'):
                    print(file)

        return file

    def read_data(self) -> pd.DataFrame:

        for file in os.listdir(self.path):

            if file.endswith('.csv'):
                self.file.append(file)
                with open(f'{self.path}\{file}', 'r') as rde_txtfile:
                    data = pd.read_csv(rde_txtfile,delimiter=',')


                return file,data

    def get_header(self) -> list:

        file,data = self.read_data()
        return list(data.columns)

    def get_dataframe(self) -> pd.DataFrame:

        file,data = self.read_data()
        col1, col2, col3, col4 = self.get_header()

        return pd.DataFrame({col1:data[col1], col2:data[col2]})

    def drop_nan_dataframe(self):

        df = self.get_dataframe()
        print(df)
        closest_index = (df['Time (s)'] - 2).abs().idxmin()

        truncated_dataframe = pd.DataFrame({'Time (s)':df['Time (s)'][closest_index:], 'WE(1).Current (A)':df['WE(1).Current (A)'][closest_index:]})
        return truncated_dataframe.dropna()





    def create_data_dictionary(self,filename, analyzed_dataframe):
        self.data_dictionary[filename] = {'Time (s)':analyzed_dataframe[0],'[H2O2]':analyzed_dataframe[1]}
        return self.data_dictionary


    def move_file_after_analysis(self):

        file, data = self.read_data()
        file_path = (f'{self.path}\{file}')

        shutil.move(os.path.join(file_path), os.path.join(f'{self.path}\Analyzed'))




