
from files import ReadData
from plots import RawPlot
from plots import CalibrationPlot
from plots import PlotDataStart
from calculations import calibration_regression
from calculations import signal_to_concentration

def read_files(file_path):

    file = ReadData(path = file_path)
    x = file.drop_nan_dataframe()
    return x

def plot_raw(data):

    plot = RawPlot(df = data)
    plot.plot_raw_data()

    calibplot = CalibrationPlot(df = data)
    calibplot.pick_calibration_points()
    calib_dataframe = calibplot.plot_picked_points()

    truncplot = PlotDataStart(df = data)
    truncplot.pick_start_point()
    df = truncplot.plot_truncated_data()

    param = calibration_regression(calib_dataframe)
    signal_to_concentration(regression_parameters=param,truncated_data=df)




if __name__ == '__main__':

    p=r'C:\Users\olegolt\OneDrive - Norwegian University of Life Sciences\PhD\Boku\RDE_data'
    file = read_files(file_path=p)

    plot_raw(data=file)