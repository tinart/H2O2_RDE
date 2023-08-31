import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tkinter import filedialog

from files import ReadData
from plots import RawPlot, CalibrationPlot, PlotDataStart, BaseLineCorrection
from calculations import calibration_regression, signal_to_concentration, baseline_regression
import tkinter as tk
# Import your plot-related classes here

class Application(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Data Analysis GUI")
        self.data = None  # Initialize data attribute
        self.raw_plotter = None
        self.baseline_corrector = None
        self.calibration_plotter = None
        self.data_start_plotter = None

        self.create_widgets()

    def create_widgets(self):
        self.tabControl = ttk.Notebook(self)
        self.raw_tab = ttk.Frame(self.tabControl)
        self.baseline_tab = ttk.Frame(self.tabControl)
        self.calibration_tab = ttk.Frame(self.tabControl)
        self.data_start_tab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.raw_tab, text='Raw Data')
        self.tabControl.add(self.baseline_tab, text='Baseline Correction')
        self.tabControl.add(self.calibration_tab, text='Calibration Plot')
        self.tabControl.add(self.data_start_tab, text='Data Start Plot')
        self.tabControl.pack(expand=1, fill="both")

        self.file_path_label = ttk.Label(self, text="Enter File Path:")
        self.file_path_label.pack()

        self.file_path_entry = ttk.Entry(self)
        self.file_path_entry.pack()

        self.browse_button = ttk.Button(self, text="Browse", command=self.browse_file)
        self.browse_button.pack()

        self.load_data_button = ttk.Button(self, text="Load Data", command=self.load_data)
        self.load_data_button.pack()

        self.raw_plot_button = ttk.Button(self.raw_tab, text="Plot Raw Data", command=self.plot_raw_data)
        self.raw_plot_button.pack()

        self.baseline_correction_button = ttk.Button(self.baseline_tab, text="Baseline Correction", command=self.baseline_correction)
        self.baseline_correction_button.pack()

        self.calibration_plot_button = ttk.Button(self.calibration_tab, text="Plot Calibration", command=self.plot_calibration)
        self.calibration_plot_button.pack()

        self.data_start_button = ttk.Button(self.data_start_tab, text="Data Start Plot", command=self.plot_data_start)
        self.data_start_button.pack()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        self.file_path_entry.delete(0, tk.END)
        self.file_path_entry.insert(0, file_path)

    def load_data(self):
        file_path = self.file_path_entry.get()
        if file_path:
            self.data = pd.read_csv(file_path)
            print("Data loaded successfully.")
        else:
            print("File path is empty.")

    def plot_raw_data(self):
        if self.data is not None:
            if self.raw_plotter is None:
                self.raw_plotter = RawPlot(df=self.data)
            self.raw_plotter.plot_raw_data()
        else:
            print("Data is not loaded yet.")

    def baseline_correction(self):
        if self.data is not None:
            if self.baseline_corrector is None:
                self.baseline_corrector = BaseLineCorrection(df=self.data)
            self.baseline_corrector.pick_baseline_points()
        else:
            print("Data is not loaded yet.")

    def plot_calibration(self):
        if self.data is not None:
            if self.calibration_plotter is None:
                self.calibration_plotter = CalibrationPlot(df=self.data)
            self.calibration_plotter.pick_calibration_points()
        else:
            print("Data is not loaded yet.")

    def plot_data_start(self):
        if self.data is not None:
            if self.data_start_plotter is None:
                self.data_start_plotter = PlotDataStart(df=self.data)
            self.data_start_plotter.pick_start_point()
        else:
            print("Data is not loaded yet.")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
