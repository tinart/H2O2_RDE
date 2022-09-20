
import pandas as pd
import os
import matplotlib.pyplot as plt


class RDEdata:

    def __init__(self, path:str):

        self.path = path

    def file_name(self):

        for file in os.listdir(self.path):
            if file.endswith('.txt'):
                return file

    def read_data(self):

        for file in os.listdir(self.path):

            if file.endswith('.txt'):
                with open(f'{self.path}\{file}', 'r') as rde_txtfile:
                    data = pd.read_csv(rde_txtfile,delimiter='\t')


                return data

    def headers(self) -> list:

        data = self.read_data()
        return list(data.columns)

    def raw_dataframe(self) -> pd.DataFrame:

        data = self.read_data()
        col1, col2 = self.headers()

        return pd.DataFrame({col1:data[col1], col2:data[col2]})







