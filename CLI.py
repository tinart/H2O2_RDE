from typing import Protocol
import pandas as pd
from ReadFile import RDEdata
from RDE_Plot import RDE_Plotter


class CLI:

    def __init__(self):
        self.df = pd.DataFrame()

    def read_rde_data(self, file_location) -> pd.DataFrame:
        d = RDEdata(path=file_location)

        return d.read_data()

    def to_string(self, nums) -> str:
        return nums.split(',')

    def plot_raw_data(self, data, H2O2):
        global plot
        plot = RDE_Plotter(raw_data=data, concentrations=self.to_string(H2O2))
        plot.plot_raw_data()
        calib_data = plot.num_to_conc()
        global df
        df = plot.dict_to_df(data_selection=calib_data)
        plot.plot_calibration_data(data_selection=df)

    @staticmethod
    def show_calibration_plot():
        df_mean = plot.calibration_mean(data_selection=df)
        plot.regression(data=df_mean)

    def pick_data_points(self, ) -> None:
        raise NotImplementedError()

    def print_data_point_list(self) -> None:
        raise NotImplementedError()

    def calibration_data_dict(self) -> dict:
        raise NotImplementedError()

    def data_dict_to_df(self, data_selection: dict) -> pd.DataFrame:
        raise NotImplementedError()

    def plot_calibration_data(self, data_selection: dict) -> pd.DataFrame:
        raise NotImplementedError()
