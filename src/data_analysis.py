import os

import pandas as pd
import shutil

from file_handling import ReadData
from data_processing import RawPlot, CalibrationPlot, PlotDataStart, BaseLineCorrection, InitialRateDetermination
from data_calculations import calibration_regression, signal_to_concentration,\
    baseline_regression, baseline_correction_function, initial_rate_regression

import seaborn as sns
import matplotlib.pyplot as plt









def move_file_after_analysis(file,data_path):


    file_path = os.path.join(data_path, file)
    shutil.move(file_path, os.path.join(data_path, 'Analyzed'))




class DataProcessing:

    def __init__(self, data_frame, file_path):
        self.data_frame = data_frame
        self.file_path = file_path
        self.bsl_data = None
        self.truncated_data = None
        self.calibrated_data = None
        self.regression_parameters = None
        self.analyzed_x = None
        self.analyzed_y = None

    def raw_plotter(self):


        raw_plotter = RawPlot(self.data_frame)
        raw_plotter.plot_raw_data()





    def baseline_correction(self):



        baseline_correction = BaseLineCorrection(self.data_frame)
        baseline_correction.pick_baseline_points()
        baseline_data = baseline_correction.baseline_data()

        baseline_coefficient, _, ypred = baseline_regression(baseline_data, self.data_frame)
        self.bsl_data = baseline_correction_function(self.data_frame, baseline_coefficient)
        baseline_correction.plot_regression_baseline()









    def calibration(self):


            calib_plotter = CalibrationPlot(self.bsl_data)
            calib_plotter.pick_calibration_points()
            self.calibrated_data = calib_plotter.plot_picked_points()
            regression_params = calibration_regression(self.calibrated_data)
            calib_plotter.plot_calibration_regression(reg_params=regression_params)
            self.regression_parameters = regression_params


    def truncated_plotter(self):

        trunc_plotter = PlotDataStart(self.bsl_data)
        trunc_plotter.pick_start_point()
        self.truncated_data = trunc_plotter.plot_truncated_data()


    def plot_analyzed_data(self):


        x, y = signal_to_concentration(regression_parameters=self.regression_parameters, truncated_data=self.truncated_data)
        calib_plotter = CalibrationPlot(self.bsl_data)
        calib_plotter.plot_signal_to_concentration(x, y)

        self.analyzed_x = x
        self.analyzed_y = y

    def data_export_handler(self):

        data_handler = ReadData(path=self.file_path)
        data_handler.move_file_after_analysis()

    def determine_initial_rate(self,dictionary):

        int_rate = InitialRateDetermination()
        int_rate.dict_to_dataframe(dictionary)
        int_rate.pick_initial_rate_points()

        initial_rate_data = int_rate.plot_picked_points()
        int_rate.plot_regression_initial_rate()




    def export_longform_dataframe(self):
        raise NotImplementedError

    def seaborn_plotter_pdf_export(self):
        raise NotImplementedError












# Specify the desired output filename


# Call the method to export the DataFrame to Excel



def seaborn_plot(dataframe):

    sns_plot = sns.lineplot(data=dataframe,x='Time (s)',y='[H2O2]',hue='Filename')
    sns_plot.get_figure().savefig('Data.pdf')

    plt.show()

def analyze(data_path):

    data_reader = ReadData(data_path)
    data_reader.get_filename_list()
    for file in data_reader.file_list:
        data_reader.read_data()

    analyzed_data_dictionary = {}
    for file in data_reader.file_list:
        try:
            data_frame = data_reader.drop_nan_dataframe(file)
        except KeyError as e:
            print(f'\033[91m A {e} occured, please check if your path is correct \033[0m')
            break

        MAX_RETRIES = 3
        processor = DataProcessing(data_frame,data_path)

        for method, error_type, description in [
            (processor.raw_plotter, Exception, "plot raw data"),
            (processor.baseline_correction, Exception, "correct baseline"),
            (processor.calibration, Exception, "calibrate data"),
            (processor.truncated_plotter, Exception, "plot truncated data"),
            (processor.plot_analyzed_data, Exception, "plot analyzed data")
        ]:
            while True:  # Keep looping until the user is satisfied
                try:
                    method()
                except Exception as e:
                    print(f"\033[91mFailed to {description} for file {file}. Error: {e}\033[0m")

                user_input = input(f"\033[91mDo you want to re-run {description} for file {file}? (y/n):\033[0m ").strip().lower()

                if user_input == 'n':
                    break  # Break the while loop and proceed to the next method
                elif user_input != 'y':
                    print("\033[91mInvalid input. Assuming you want to proceed to the next step.\033[0m")
                    break
        x = processor.analyzed_x
        y = processor.analyzed_y

        analyzed_data_dictionary[file] = {'Time (s)': x - x.iloc[0], '[H2O2]': y}

        #processor.determine_initial_rate(analyzed_data_dictionary)

        move_file_after_analysis(file,data_path)




    exported_data = data_reader.create_longform_dataframe(data_dictionary=analyzed_data_dictionary)

    seaborn_plot(exported_data)


data_path = r'C:\Users\olegolt\OneDrive - Norwegian University of Life Sciences\PhD\Boku\Experiments\Sensor\b\Selection'
#analyze(data_path)
