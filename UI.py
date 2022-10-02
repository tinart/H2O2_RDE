from typing import Protocol
import pandas as pd


class UI(Protocol):

    def read_rde_data(self, file_location) -> pd.DataFrame:
        raise NotImplementedError()


    def pick_data_points(self,) -> None:
        raise NotImplementedError()

    def print_data_point_list(self) -> None:
        raise NotImplementedError()

    def calibration_data_dict(self) -> dict:
        raise NotImplementedError()

    def data_dict_to_df(self, data_selection: dict) -> pd.DataFrame:
        raise NotImplementedError()

    def plot_calibration_data(self, data_selection: dict) -> pd.DataFrame:
        raise NotImplementedError()




