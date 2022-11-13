import tkinter as tk
from tkinter import ttk, Button
from datetime import datetime
from CLI import CLI
from RDE_Plot import RDE_Plotter


class ExperimentInfo(ttk.LabelFrame):

    def __init__(self, container):
        super().__init__(container, borderwidth=1, relief='sunken', text='Experiment Information')

        self.__create_widgets()

    def __create_widgets(self):
        tk.Label(self, text='Experiment Name:').grid(column=0, row=0, sticky=tk.W)
        self.Exp_Name_Entry = tk.Entry(self)
        self.Exp_Name_Entry.grid(column=1, row=0, sticky=tk.W)

        tk.Label(self, text='Date:').grid(column=0, row=1, sticky=tk.W)

        self.Exp_Date_Entry = tk.Entry(self)
        now = datetime.now()
        dt_string = now.strftime('%y%m%d')
        self.Exp_Date_Entry.insert(1, dt_string)
        self.Exp_Date_Entry.grid(column=1, row=1, sticky=tk.W)

        tk.Label(self, text='Directrory Path').grid(column=0, row=2, sticky=tk.W)
        self.Exp_Path_Entry = tk.Entry(self)
        self.Exp_Path_Entry.insert(1,r'C:\Users\olegolt\OneDrive - Norwegian University of Life Sciences\PhD\Boku\RDE_data')
        self.Exp_Path_Entry.grid(column=1, row=2, sticky=tk.W)

        tk.Label(self, text='H2O2 Concentrations').grid(column=0, row=4, sticky=tk.W)
        self.H2O2_concentrations_entry = tk.Entry(self)
        self.H2O2_concentrations_entry.grid(column=1, row=4, sticky=tk.W)

        Exp_Load_Data_Button: Button = tk.Button(self, text='Plot RDE Data', command=self.load_data)
        Exp_Load_Data_Button.grid(column=0, row=5, sticky=tk.W)

    def load_data(self):
        path: str = self.Exp_Path_Entry.get()
        H2O2_concentrations: str = str(self.H2O2_concentrations_entry.get())

        d = CLI().read_rde_data(file_location=path)
        CLI().plot_raw_data(data=d, H2O2=H2O2_concentrations)


class Calibration(ttk.LabelFrame):

    def __init__(self, container):
        super().__init__(container, borderwidth=1, relief='sunken', text='Calibration')

        self.__create_widgets()

    def __create_widgets(self):

        tk.Button(self,text='Check Calibration', command=self.calibration).grid(
            column=0, row=0,sticky=tk.W
        )


    def calibration(self):

        CLI().show_calibration_plot()


    def pick_data_start(self):
        pass










class App(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title('Stopped Flow Analysis')
        self.geometry('500x600')
        self.resizable(True, True)
        self.__create_widgets()

    def __create_widgets(self):
        Exp_Info = ExperimentInfo(self)
        Exp_Info.grid(column=0, row=0, columnspan=3, sticky=tk.EW)

        Calib = Calibration(self)
        Calib.grid(column=0, row=1, columnspan=3, sticky=tk.EW)


