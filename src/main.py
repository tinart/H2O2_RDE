import os

import pandas as pd

from file_handling import ReadData
from data_processing import RawPlot, CalibrationPlot, PlotDataStart, BaseLineCorrection, InitialRateDetermination
from data_calculations import calibration_regression, signal_to_concentration,\
    baseline_regression, baseline_correction_function, initial_rate_regression

import seaborn as sns
import matplotlib.pyplot as plt

from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Alignment




data_reader = None

def read_files(file_path):
    global data_reader
    if data_reader is None:
        data_reader = ReadData(path=file_path)

    data_reader.create_new_folder()
    cleaned_data = data_reader.drop_nan_dataframe()
    return cleaned_data

def get_file_name(file_path):
    global data_reader
    if data_reader is None:
        data_reader = ReadData(path=file_path)
    file = data_reader.get_filename()
    return file

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





def data_export_handling(file_path):

    data_handler = ReadData(path=file_path)
    data_handler.move_file_after_analysis()

def create_longform_dataframe(data_dictionary, file_path):
    # Create an empty DataFrame
    df = pd.DataFrame(columns=['Filename', 'Time (s)', '[H2O2]'])

    # Iterate through the dictionary and append 'a' and 'y' values as rows
    for filename, values in data_dictionary.items():
        if 'Time (s)' in values and '[H2O2]' in values:
            x_values = values['Time (s)']
            y_values = values['[H2O2]']
            temp_df = pd.DataFrame({'Filename': [filename] * len(x_values), 'Time (s)': x_values, '[H2O2]': y_values})
            df = pd.concat([df, temp_df], ignore_index=True)


    return df


def export_dataframe_to_excel(df, output_filename,path):
    """
    Export a DataFrame with multiple filenames to an Excel file with separate sheets.

    Args:
        df (pd.DataFrame): The DataFrame with columns 'Filename', 'Time (s)', and '[H2O2]'.
        output_filename (str): The desired output filename for the Excel file.
    """
    # Create a new Excel workbook
    os.chdir(f'{path}\Analyzed')
    wb = Workbook()

    # Loop through each unique filename and export its data to a separate sheet
    for filename in df['Filename'].unique():
        # Create a new worksheet for each filename
        ws = wb.create_sheet(title=filename)

        # Set column widths
        ws.column_dimensions['A'].width = 30
        ws.column_dimensions['B'].width = 15
        ws.column_dimensions['C'].width = 15

        # Merge cells for the "Filename" column and place it in the first cell
        ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=3)
        cell = ws.cell(row=1, column=1)
        cell.value = filename
        cell.alignment = Alignment(horizontal='center', vertical='center')

        # Filter the data for the current filename and place "Time (s)" and "[H2O2]" columns underneath
        filtered_data = df[df['Filename'] == filename][['Time (s)', '[H2O2]']]
        for row in dataframe_to_rows(filtered_data, index=False, header=False):
            ws.append(row)

    # Remove the default empty sheet created when the workbook is initialized
    if 'Sheet' in wb.sheetnames:
        wb.remove(wb['Sheet'])

    # Save the workbook to an Excel file
    wb.save(output_filename)

    print(f'Data has been exported to {output_filename}')


# Specify the desired output filename


# Call the method to export the DataFrame to Excel



def seaborn_plot(dataframe):

    sns.lineplot(data=dataframe,x='Time (s)',y='[H2O2]',hue='Filename')

    plt.show()

def analyze(data_path):
    data_reader = ReadData(data_path)
    total_files = data_reader.count_files()
    if total_files == 0:
        print('No .csv files found in directory, check filepath.')
    else:
        output_filename = 'data.xlsx'
        analyzed_data_dictionary = {}

        for _ in range(total_files):


            data_frame = read_files(file_path=data_path)

            processor = DataProcessing(data_frame,data_path)
            processor.raw_plotter()
            processor.baseline_correction()
            processor.calibration()
            processor.truncated_plotter()
            processor.plot_analyzed_data()

            x = processor.analyzed_x
            y = processor.analyzed_y
            file = get_file_name(data_path)
            analyzed_data_dictionary[file] = {'Time (s)': x - x.iloc[0], '[H2O2]': y}

            processor.determine_initial_rate(analyzed_data_dictionary)




        exported_data = create_longform_dataframe(data_dictionary=analyzed_data_dictionary, file_path=data_path)

        seaborn_plot(exported_data)

if __name__ == '__main__':
    data_path = r'C:\Users\olegolt\OneDrive - Norwegian University of Life Sciences\PhD\Boku\Experiments\Sensor\b\Selection'
    analyze(data_path)