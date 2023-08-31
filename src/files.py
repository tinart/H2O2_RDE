
import pandas as pd
import os
import matplotlib.pyplot as plt


class ReadData:

    def __init__(self, path:str):

        self.path = path

    def get_filename(self):

        for file in os.listdir(self.path):
            if file.endswith('.txt'):
                return file

    def read_data(self):

        for file in os.listdir(self.path):

            if file.endswith('.csv'):
                with open(f'{self.path}\{file}', 'r') as rde_txtfile:
                    data = pd.read_csv(rde_txtfile,delimiter=',')


                return data

    def get_header(self) -> list:

        data = self.read_data()
        return list(data.columns)

    def get_dataframe(self) -> pd.DataFrame:

        data = self.read_data()
        col1, col2, col3, col4 = self.get_header()

        return pd.DataFrame({col1:data[col1], col2:data[col2]})

    def drop_nan_dataframe(self):

        df = self.get_dataframe()
        return df.dropna()







