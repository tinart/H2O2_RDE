from files import ReadData
from plots import RawPlot, CalibrationPlot, PlotDataStart, BaseLineCorrection
from calculations import calibration_regression, signal_to_concentration, baseline_regression, baseline_correction_function
from gui_app import Application
import tkinter as tk

def read_files(file_path):
    data_reader = ReadData(path=file_path)
    cleaned_data = data_reader.drop_nan_dataframe()
    return cleaned_data

def process_and_plot(data_frame):
    raw_plotter = RawPlot(data_frame)
    raw_plotter.plot_raw_data()

    baseline_correction = BaseLineCorrection(data_frame)
    baseline_correction.pick_baseline_points()
    baseline_data = baseline_correction.baseline_data()

    baseline_coefficient = baseline_regression(baseline_data)
    bsl_data = baseline_correction_function(data_frame,baseline_coefficient)


    calib_plotter = CalibrationPlot(bsl_data)
    calib_plotter.pick_calibration_points()
    calib_dataframe = calib_plotter.plot_picked_points()

    trunc_plotter = PlotDataStart(bsl_data)
    trunc_plotter.pick_start_point()
    truncated_data = trunc_plotter.plot_truncated_data()

    regression_params = calibration_regression(calib_dataframe)
    signal_to_concentration(regression_parameters=regression_params, truncated_data=truncated_data)



if __name__ == '__main__':
    data_path = r'C:\Users\olegolt\OneDrive - Norwegian University of Life Sciences\PhD\Boku\Experiments\Sensor\230829_NcAA9C_CN_0-800uM_XG_MOPS_pH7_30C'
    data_frame = read_files(file_path=data_path)

    process_and_plot(data_frame)