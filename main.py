
from ReadFile import RDEdata
from RDE_Plot import RDE_Plotter
import matplotlib.pyplot as plt
import numpy as np
from GUI import App

def read_rde_data(path_loc):
    d = RDEdata(path=path_loc)

    return d.read_data()

def plot(data):

    l = ['20', '40', '60', '80', '100', '120']

    plot = RDE_Plotter(raw_data=data,concentrations=l)

    plot.plot_raw_data()
    plot.print_list()
    calib_data = plot.num_to_conc()
    df = plot.dict_to_df(data_selection=calib_data)

    plot.plot_calibration_data(data_selection=df)
    df = plot.calibration_mean(data_selection=df)
    plot.regression(data=df)
    plot.plot_raw_start()
    plot.data_start()
    plot.plot_truncated()




if __name__ == '__main__':

    app = App()

    app.mainloop()

    #p = r'C:\Users\olegolt\OneDrive - Norwegian University of Life Sciences\PhD\Boku\RDE_data'


    #raw_data=read_rde_data(path_loc =p)
    #plot(data=raw_data)

    #plt.show()




