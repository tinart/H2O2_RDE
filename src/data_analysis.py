import os

import pandas as pd
import numpy as np
import shutil

from file_handling import ReadData, time_function
from data_processing import RawPlot, CalibrationPlot, PlotDataStart, BaseLineCorrection, InitialRateDetermination
from data_calculations import calibration_regression, signal_to_concentration, \
    baseline_regression, baseline_correction_function, rolling_regression

import seaborn as sns
import matplotlib.pyplot as plt


def move_file_after_analysis(file, data_path):
    file_path = os.path.join(data_path, file)
    shutil.move(file_path, os.path.join(data_path, 'Analyzed'))


class DataProcessing:

    def __init__(self, data_frame, file_path, concentrations):
        self.data_frame = data_frame
        self.file_path = file_path
        self.concentrations = concentrations
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
        print(self.concentrations)
        calib_plotter = CalibrationPlot(self.bsl_data, self.concentrations)
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
        x, y = signal_to_concentration(regression_parameters=self.regression_parameters,
                                       truncated_data=self.truncated_data)
        calib_plotter = CalibrationPlot(self.bsl_data, self.concentrations)
        calib_plotter.plot_signal_to_concentration(x, y)

        self.analyzed_x = x
        self.analyzed_y = y

    def data_export_handler(self):
        data_handler = ReadData(path=self.file_path)
        data_handler.move_file_after_analysis()

    def export_longform_dataframe(self):
        raise NotImplementedError

    def seaborn_plotter_pdf_export(self):
        raise NotImplementedError


# Specify the desired output filename


# Call the method to export the DataFrame to Excel


def seaborn_plot(dataframe):
    sns_plot = sns.lineplot(data=dataframe, x='Time (s)', y='[H2O2]', hue='Filename')
    sns_plot.get_figure().savefig('Data.pdf')

    plt.show()


def analyze(data_path, concentrations):
    data_reader = ReadData(data_path)
    data_reader.create_new_folder()
    data_reader.get_filename_list()
    for file in data_reader.file_list:
        data_reader.read_data()

    analyzed_data_dictionary = {}
    for file in data_reader.file_list:
        try:
            data_frame = data_reader.drop_nan_dataframe(file)
        except KeyError as e:
            print(f'A {e} occured, please check if your path is correct')
            break

        processor = DataProcessing(data_frame, data_path, concentrations)
        processor.raw_plotter()
        for method, error_type, description in [

            (processor.baseline_correction, Exception, "correct baseline"),
            (processor.calibration, Exception, "calibrate data"),
            (processor.truncated_plotter, Exception, "plot truncated data"),

        ]:


            while True:  # Keep looping until the user is satisfied
                try:
                    method()
                except Exception as e:
                    print(f"Failed to {description} for file {file}. Error: {e}")

                user_input = input(f"Are you satisfied with {description} for file {file}? (y/n)").strip().lower()

                if user_input == 'y':
                    break  # Break the while loop and proceed to the next method
                elif user_input != 'n':
                    print("Invalid input. Assuming you want to proceed to the next step.")
                    break

        processor.plot_analyzed_data()
        x = processor.analyzed_x
        y = processor.analyzed_y

        analyzed_data_dictionary[file] = {'Time (s)': x - x.iloc[0], '[H2O2]': y}

        # processor.determine_initial_rate(analyzed_data_dictionary)

        move_file_after_analysis(file, data_path)

    exported_data = data_reader.create_longform_dataframe(data_dictionary=analyzed_data_dictionary)

    seaborn_plot(exported_data)


def determine_initial_rate(df):
    int_rate = InitialRateDetermination()
    int_rate.dataframe(df)
    int_rate.pick_initial_rate_points()

    initial_rate_data = int_rate.plot_picked_points()
    coef, intercept = int_rate.plot_regression_initial_rate()
    return coef, intercept


def intial_rate_manual(input_filename, dir_path):
    data = pd.read_csv(input_filename)
    grouped_dataframes = {name: group for name, group in data.groupby('Filename')}

    initial_rates_analysis = pd.DataFrame()

    for filename, dataframe in grouped_dataframes.items():
        print(f'processing{filename}')
        coef, intecept = determine_initial_rate(df=dataframe)

        coef = coef[0] if isinstance(coef, (list, np.ndarray)) else coef
        intecept = intecept[0] if isinstance(intecept, (list, np.ndarray)) else intecept

        analysis = pd.DataFrame({
            'Filename': filename,
            'Coefficient': coef,
            'Intercept': intecept
        })
        initial_rates_analysis = pd.concat([initial_rates_analysis, analysis], ignore_index=True)
    os.chdir(path=dir_path)
    initial_rates_analysis.to_csv('Intial_Rates.csv')


@time_function
def intial_rate_analysis(input_filename):
    data = pd.read_csv(input_filename)

    results = data.groupby('Filename').apply(rolling_regression, window_size=5)
    return data, results


def plot_precomputed_rolling_regression_facet_grid(data, regression_results):
    # Get the unique filenames to determine the grid size
    filenames = data['Filename'].unique()
    num_files = len(filenames)

    # Define the number of rows and columns for the subplot grid
    num_columns = int(np.ceil(np.sqrt(num_files)))
    num_rows = int(np.ceil(num_files / num_columns))

    # Create a figure with subplots
    fig, axs = plt.subplots(num_rows, num_columns, figsize=(num_columns * 5, num_rows * 5), squeeze=False)

    # Flatten the axes array for easy iteration
    axs = axs.flatten()

    # Iterate over each unique file to create a subplot
    for idx, filename in enumerate(filenames):
        group = data[data['Filename'] == filename]

        # Retrieve the precomputed slope and intercept for this group
        slope, intercept, (start_time, end_time) = regression_results.get(filename, (None, None, (None, None)))

        if slope is not None and start_time is not None and end_time is not None:
            # Create a range of time values for plotting the regression line
            regression_time = np.linspace(start_time, end_time, 100)
            regression_concentration = intercept + slope * regression_time

            # Plot the original data points
            axs[idx].scatter(group['Time (s)'], group['[H2O2]'], label='Data Points', alpha=0.5)

            # Plot the regression line
            axs[idx].plot(regression_time, regression_concentration, color='red', label='Regression Line', linewidth=2)

            # Highlight the window of the steepest slope
            axs[idx].axvspan(start_time, end_time, color='yellow', alpha=0.3, label='Window of Steepest Slope')

            axs[idx].set_title(f'File: {filename}')
            axs[idx].set_xlabel('Time (s)')
            axs[idx].set_ylabel('[H2O2]')
            axs[idx].legend()
            axs[idx].grid(True)
        else:
            axs[idx].text(0.5, 0.5, 'No valid regression\nfor this file',
                          horizontalalignment='center', verticalalignment='center',
                          transform=axs[idx].transAxes)
            axs[idx].set_title(f'File: {filename}')
            axs[idx].set_xlabel('Time (s)')
            axs[idx].set_ylabel('[H2O2]')
            axs[idx].grid(True)

    # Remove any unused subplots
    for ax in axs[num_files:]:
        ax.remove()

    plt.tight_layout()
    plt.show()


data_path = r'C:\Users\olegolt\OneDrive - Norwegian University of Life Sciences\PhD\Boku\Experiments\Sensor\b\Selection'
# analyze(data_path)
