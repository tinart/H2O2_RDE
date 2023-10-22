import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from data_calculations import calibration_regression, signal_to_concentration,\
    baseline_regression, baseline_correction_function, calibration_mean, initial_rate_regression


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
        plt.title('Raw Data')
        plt.xlabel(col_names[0])
        plt.ylabel(col_names[1])
        plt.show()

class BaseLineCorrection:

    def __init__(self, df):
        self.df = df
        self.baseline = {}
        self.x = []
        self.y = []

    @property
    def get_colnames(self) -> list:
        return [col for col in self.df.columns]

    def baseline_correction_picker(self, event) -> None:
        column_names = self.get_colnames
        ind = event.ind

        x = np.take(self.df[column_names[0]], ind)
        y = np.take(self.df[column_names[1]], ind)



        self.x.extend(x)
        self.y.extend(y)

    def pick_baseline_points(self):
        col_names = self.get_colnames

        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        col = ax1.scatter(self.df[col_names[0]], self.df[col_names[1]], picker=True)

        fig.canvas.mpl_connect('pick_event', self.baseline_correction_picker)
        plt.title('Select baseline values')

        plt.show()

    def baseline_data(self) -> list:
        self.baseline['Values'] = {'x':self.x,'y':self.y}
        return self.baseline

    def plot_regression_baseline(self):

        data = self.baseline_data()
        print(data)

        bsl_coeff, _, ypred = baseline_regression(data,self.df)

        x = np.array(data['Values']['x']).reshape(-1, 1)
        y = np.array(data['Values']['y']).reshape(-1, 1)


        plt.scatter(self.df['Time (s)'],self.df['WE(1).Current (A)'])
        plt.scatter(x, y, color='red')
        plt.plot(x, ypred)
        plt.title('Selected baseline regression')
        plt.show()




class CalibrationPlot:

    def __init__(self, df):
        self.df = df
        self.n = 1
        self.raw_data_list = {}
        self.concentrations = ['0','20','40','60','80','100']




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
        plt.title('Pick claibration data plateus')

        plt.show()

    def num_to_conc(self) -> dict:
        return dict(zip(self.concentrations, list(self.raw_data_list.values())))

    def dict_to_df(self) -> pd.DataFrame:


        df = pd.DataFrame()
        data = self.num_to_conc()
        print('Hello')
        print(data.keys())

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
        plt.title('Picked calibration points')
        plt.show()

        return data

    def plot_calibration_regression(self,reg_params):

        data = self.dict_to_df()
        coef, intercept, ypred = reg_params
        calib_mean = calibration_mean(data_selection=data)


        x = np.array(calib_mean['Concentration Mean']).reshape((-1, 1))
        y = np.array(calib_mean['Signal Mean']).reshape((-1, 1))


        plt.scatter(x, y, color='red')
        plt.plot(x, ypred)
        plt.title('Calibration Plot')
        plt.show()
        print(f'Slope:{coef} and intercept:{intercept}')

    def plot_signal_to_concentration(self,x,y):


        plt.plot(x,y)
        plt.show()





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
        plt.title('Zoom inn and pick one start point')

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

        df = pd.DataFrame({'x':x[start:],'y':y[start:]})
        return df

class InitialRateDetermination:

    def __init__(self):

        self.df = None
        self.int_rate = {}
        self.x = []
        self.y = []

    def dict_to_dataframe(self,dictionary):

        df = pd.DataFrame(columns=['Filename', 'Time (s)', '[H2O2]'])

        # Iterate through the dictionary and append 'a' and 'y' values as rows
        for filename, values in dictionary.items():
            if 'Time (s)' in values and '[H2O2]' in values:
                x_values = values['Time (s)']
                y_values = values['[H2O2]']
                temp_df = pd.DataFrame(
                    {'Filename': [filename] * len(x_values), 'Time (s)': x_values, '[H2O2]': y_values})
                df = pd.concat([df, temp_df], ignore_index=True)


        self.df = df

    @property
    def get_colnames(self) -> list:
        return [col for col in self.df.columns]

    def initial_rate_picker(self, event) -> None:
        column_names = self.get_colnames
        ind = event.ind

        x = np.take(self.df[column_names[1]], ind)
        y = np.take(self.df[column_names[2]], ind)

        self.x.extend(x)
        self.y.extend(y)


    def pick_initial_rate_points(self):
        col_names = self.get_colnames

        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        col = ax1.scatter(self.df[col_names[1]], self.df[col_names[2]], picker=True)

        fig.canvas.mpl_connect('pick_event', self.initial_rate_picker)
        plt.title('Select initial rate')

        plt.show()


    def plot_picked_points(self):


        col_names = self.get_colnames
        plt.scatter(self.df[col_names[1]], self.df[col_names[2]], s=3)

        plt.scatter(self.x,self.y, s=5, color='red')
        plt.title('Picked calibration points')
        plt.show()



    def initial_rate_data(self) -> list:
        self.int_rate['Values'] = {'x':self.x,'y':self.y}
        print(self.int_rate)
        return self.int_rate

    def plot_regression_initial_rate(self):

        data = self.initial_rate_data()


        bsl_coeff, _, ypred = initial_rate_regression(self.x,self.y)

        x = np.array(data['Values']['x']).reshape(-1, 1)
        y = np.array(data['Values']['y']).reshape(-1, 1)

        plt.scatter(self.df['Time (s)'], self.df['[H2O2]'])
        plt.scatter(x, y, color='red')
        plt.plot(x, ypred)
        plt.title('Selected baseline regression')
        plt.show()






