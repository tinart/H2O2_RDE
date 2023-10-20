import os

import pandas as pd

from file_handling import ReadData
from data_processing import RawPlot, CalibrationPlot, PlotDataStart, BaseLineCorrection
from data_calculations import calibration_regression, signal_to_concentration,\
    baseline_regression, baseline_correction_function

import seaborn as sns
import matplotlib.pyplot as plt

from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Alignment




def read_files(file_path):

    data_reader = ReadData(path=file_path)
    data_reader.create_new_folder()
    cleaned_data = data_reader.drop_nan_dataframe()
    return cleaned_data

def get_file_name(file_path):
    data_reader = ReadData(path=file_path)
    file = data_reader.get_filename()
    return file

class DataProcessing:

    def __init__(self):
        pass

    def raw_plotter(self):
        raise NotImplementedError

    def baseline_correction(self):
        raise NotImplementedError

    def calibration(self):
        raise NotImplementedError

    def data_export_handler(self):
        raise NotImplementedError

    def create_longform_dataframe(self):
        raise NotImplementedError

    def export_longform_dataframe(self):
        raise NotImplementedError

    def seaborn_plotter_pdf_export(self):
        raise NotImplementedError



def process_and_plot(data_frame):
    raw_plotter = RawPlot(data_frame)
    raw_plotter.plot_raw_data()

    baseline_correction = BaseLineCorrection(data_frame)
    baseline_correction.pick_baseline_points()
    baseline_data = baseline_correction.baseline_data()

    baseline_coefficient, ypred = baseline_regression(baseline_data, data_frame)
    bsl_data = baseline_correction_function(data_frame,baseline_coefficient)
    baseline_correction.plot_regression_baseline()



    calib_plotter = CalibrationPlot(bsl_data)
    calib_plotter.pick_calibration_points()
    calib_dataframe = calib_plotter.plot_picked_points()


    trunc_plotter = PlotDataStart(bsl_data)
    trunc_plotter.pick_start_point()
    truncated_data = trunc_plotter.plot_truncated_data()


    regression_params = calibration_regression(calib_dataframe)
    calib_plotter.plot_calibration_regression(reg_params=regression_params)

    x, y = signal_to_concentration(regression_parameters=regression_params, truncated_data=truncated_data)
    calib_plotter.plot_signal_to_concentration(x,y)
    return x,y



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
            print(df)

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
    print('Hello')
    plt.show()

def analyze(data_path):

    data_file = ReadData(data_path).count_files()
    output_filename = 'data.xlsx'

    analyzed_data_dictionary = {}

    while data_file != 0:
        data_frame = read_files(file_path=data_path)
        x,y = process_and_plot(data_frame)
        file = get_file_name(data_path)
        print(x.iloc[0])
        analyzed_data_dictionary[file] = {'Time (s)': x-x.iloc[0], '[H2O2]': y}
        data_export_handling(file_path=data_path)
        data_file -= 1



    exported_data = create_longform_dataframe(data_dictionary=analyzed_data_dictionary, file_path=data_path)
    export_dataframe_to_excel(exported_data,output_filename,data_path)
    seaborn_plot(exported_data)





if __name__ == '__main__':
    data_path = r'C:\Users\olegolt\OneDrive - Norwegian University of Life Sciences\PhD\Boku\Experiments\Sensor\231014_NcAA9C_No_Substrate_Buffer\Test'

    analyze(data_path)