import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


class RDE_Plotter:

    def __init__(self, raw_data, concentrations: list):
        self.raw_data = raw_data
        self.raw_data_list = {}
        self.calibration_list = {}
        self.concentrations = concentrations
        self.n = 1
        self.start = []

    def __repr__(self):
        pass

    def onpick(self, event) -> None:
        ind = event.ind

        x = np.take(self.raw_data['Time'], ind)
        y = np.take(self.raw_data['Current [nA]'], ind)

        self.raw_data_list[f'{self.n}'] = {'x': x, 'y': y}
        self.n += 1

    def onpick_start(self, event) -> None:

        ind = event.ind

        x = np.take(self.raw_data['Time'], ind)
        y = np.take(self.raw_data['Current [nA]'], ind)

        self.start.append([x])



    def data_start(self):

        start = (np.where(self.raw_data['Time'] == float(self.start[0][0])))
        return start[0][0]

    def plot_truncated(self):
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        col = ax1.scatter(self.raw_data['Time'][self.data_start():], self.raw_data['Current [nA]'][self.data_start():], picker=True)



    def plot_raw_start(self):
            fig = plt.figure()
            ax1 = fig.add_subplot(111)
            col = ax1.scatter(self.raw_data['Time'], self.raw_data['Current [nA]'], picker=True)

            fig.canvas.mpl_connect('pick_event', self.onpick_start)

            plt.show()




    def print_list(self):
        print(self.raw_data_list)

    def num_to_conc(self) -> dict:
        return dict(zip(self.concentrations, list(self.raw_data_list.values())))

    def plot_raw_data(self):
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        col = ax1.scatter(self.raw_data['Time'], self.raw_data['Current [nA]'], picker=True)

        fig.canvas.mpl_connect('pick_event', self.onpick)

        plt.show()

    def dict_to_df(self, data_selection: dict) -> pd.DataFrame:
        df = pd.DataFrame()
        data = data_selection

        for n in self.concentrations:
            x = data[n]['x']
            y = data[n]['y']

            df1 = pd.DataFrame({'Concentration': n, 'Time': x, 'Signal': y})
            df = pd.concat([df, df1], ignore_index=True)
        return df

    def plot_calibration_data(self, data_selection: dict):
        data = data_selection
        plt.scatter(self.raw_data['Time'], self.raw_data['Current [nA]'], s=3)
        plt.scatter(data['Time'], data['Signal'], s=5, color='red')

        plt.show()

    def calibration_mean(self, data_selection):
        data = data_selection
        data['Concentration'] = pd.to_numeric(data['Concentration'])
        df = data.groupby('Concentration', as_index=False).mean()
        df = df.rename(columns={'Concentration': 'Concentration Mean', 'Time': 'Time Mean', 'Signal': 'Signal Mean'})

        return df

    def regression(self, data):
        df = data
        lr = LinearRegression()
        x = np.array(df['Concentration Mean']).reshape((-1, 1))
        y = np.array(df['Signal Mean']).reshape((-1, 1))

        lr.fit(x, y)
        ypred = lr.predict(x)

        plt.scatter(x, y, color='red')
        plt.plot(x, ypred)
        plt.show()
        print(f'Slope:{lr.coef_} and intercept:{lr.intercept_}')

        return (lr.coef_, lr.intercept_)


