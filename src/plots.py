import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class RawPlot:

    def __init__(self, df):
        self.df = df

    @property
    def get_colnames(self) -> list:
        return [col for col in self.df.columns]

    def plot_raw_data(self):
        col_names = self.get_colnames
        data = self.df
        plt.plot(
            data[col_names[0]],
            data[col_names[1]]
        )
        plt.xlabel(col_names[0])
        plt.ylabel(col_names[1])
        plt.show()

class BaseLineCorrection:

    def __init__(self, df):
        self.df = df
        self.baseline = {}
        self.n = 1
    @property
    def get_colnames(self) -> list:
        return [col for col in self.df.columns]

    def baseline_correction_picker(self, event) -> None:
        column_names = self.get_colnames
        ind = event.ind

        x = np.take(self.df[column_names[0]], ind)
        y = np.take(self.df[column_names[1]], ind)


        self.baseline[f'{self.n}'] = {'x': x, 'y': y}
        self.n += 1

    def pick_baseline_points(self):
        col_names = self.get_colnames

        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        col = ax1.scatter(self.df[col_names[0]], self.df[col_names[1]], picker=True)

        fig.canvas.mpl_connect('pick_event', self.baseline_correction_picker)

        plt.show()

    def baseline_data(self) -> list:
        return self.baseline


class CalibrationPlot:

    def __init__(self, df):
        self.df = df
        self.n = 1
        self.raw_data_list = {}
        self.concentrations = ['20','40','60','80','100','120']

    @property
    def get_colnames(self) -> list:
        return [col for col in self.df.columns]

    def calibration_picker(self, event) -> None:
        col_names = self.get_colnames
        ind = event.ind

        x = np.take(self.df[col_names[0]], ind)
        y = np.take(self.df[col_names[1]], ind)

        self.raw_data_list[f'{self.n}'] = {'x': x, 'y': y}
        self.n += 1


    def pick_calibration_points(self):
        col_names = self.get_colnames

        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        col = ax1.scatter(self.df[col_names[0]], self.df[col_names[1]], picker=True)

        fig.canvas.mpl_connect('pick_event', self.calibration_picker)

        plt.show()

    def num_to_conc(self) -> dict:
        return dict(zip(self.concentrations, list(self.raw_data_list.values())))

    def dict_to_df(self) -> pd.DataFrame:
        df = pd.DataFrame()
        data = self.num_to_conc()

        for n in self.concentrations:
            x = data[n]['x']
            y = data[n]['y']

            df1 = pd.DataFrame({'Concentration': n, 'Time': x, 'Signal': y})
            df = pd.concat([df, df1], ignore_index=True)
        return df

    def plot_picked_points(self):

        data = self.dict_to_df()
        col_names = self.get_colnames
        plt.scatter(self.df[col_names[0]], self.df[col_names[1]], s=3)

        plt.scatter(data['Time'],data['Signal'], s=5, color='red')
        plt.show()

        return data


class PlotDataStart:

    def __init__(self, df):
        self.df =df
        self.start = []

    def get_colnames(self) -> list:
        return [col for col in self.df.columns]

    def data_start_picker(self, event) -> None:
        ind = event.ind

        col_names = self.get_colnames()

        x = np.take(self.df[col_names[0]], ind)
        y = np.take(self.df[col_names[1]], ind)

        self.start.append([x])

    def pick_start_point(self) -> None:
        col_names = self.get_colnames()

        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        col = ax1.scatter(self.df[col_names[0]], self.df[col_names[1]], picker=True)

        fig.canvas.mpl_connect('pick_event', self.data_start_picker)

        plt.show()

    def get_data_start(self):
        col_names = self.get_colnames()

        start = (np.where(self.df[col_names[0]] == float(self.start[0][0])))
        return start[0][0]

    def plot_truncated_data(self):

        start = self.get_data_start()
        col_names = self.get_colnames()

        x = self.df[col_names[0]]
        y = self.df[col_names[1]]

        plt.plot(x[start:], y[start:])
        plt.show()

        df = pd.DataFrame({'x':x,'y':y})
        return df




class CalibratedDataPlot:
    pass
