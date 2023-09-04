from file_handling import ReadData
from data_processing import RawPlot, CalibrationPlot, PlotDataStart, BaseLineCorrection
from data_calculations import calibration_regression, signal_to_concentration,\
    baseline_regression, baseline_correction_function




def read_files(file_path):

    data_reader = ReadData(path=file_path)
    data_reader.create_new_folder()
    cleaned_data = data_reader.drop_nan_dataframe()
    return cleaned_data

def process_and_plot(data_frame):
    raw_plotter = RawPlot(data_frame)
    raw_plotter.plot_raw_data()

    baseline_correction = BaseLineCorrection(data_frame)
    baseline_correction.pick_baseline_points()
    baseline_data = baseline_correction.baseline_data()

    baseline_coefficient = baseline_regression(baseline_data, data_frame)
    bsl_data = baseline_correction_function(data_frame,baseline_coefficient)


    calib_plotter = CalibrationPlot(bsl_data)
    calib_plotter.pick_calibration_points()
    calib_dataframe = calib_plotter.plot_picked_points()

    trunc_plotter = PlotDataStart(bsl_data)
    trunc_plotter.pick_start_point()
    truncated_data = trunc_plotter.plot_truncated_data()

    regression_params = calibration_regression(calib_dataframe)
    signal_to_concentration(regression_parameters=regression_params, truncated_data=truncated_data)
    return truncated_data



def data_export_handling(file_path):

    data_handler = ReadData(path=file_path)
    data_handler.move_file_after_analysis()


def analyze(data_path):
    data_frame = read_files(file_path=data_path)
    data_file = ReadData(data_path).count_files()

    analyzed_data_dictionary = {}

    while data_file != 0:
        print(data_file)
        data = process_and_plot(data_frame)
        data_export_handling(file_path=data_path)
        data_file -= 1




if __name__ == '__main__':
    data_path = r'C:\Users\olegolt\OneDrive - Norwegian University of Life Sciences\PhD\Boku\Experiments\Sensor\230829_NcAA9C_CN_0-800uM_XG_MOPS_pH7_30C'

    analyze(data_path)