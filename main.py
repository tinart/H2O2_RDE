
from ReadFile import RDEdata
from RDE_Plot import RDE_Plotter
import matplotlib.pyplot as plt
import numpy as np

def read_rde_data(path_loc):
    d = RDEdata(path=path_loc)

    return d.read_data()

def plot(data):

    plot = RDE_Plotter()

    plot.plot_raw_data(raw_data=data)



if __name__ == '__main__':

    p = r'C:\Users\olegolt\OneDrive - Norwegian University of Life Sciences\PhD\Boku\RDE_data'


    raw_data=read_rde_data(path_loc =p)
    #plot(data=raw_data)

    def onpick(event):
        ind = event.ind

        print('onpick3 scatter:', ind, np.take(data['Time'], ind), np.take(data['Current [nA]'], ind))

    data = raw_data
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    col = ax1.scatter(data['Time'], data['Current [nA]'], picker=True)
    # fig.savefig('pscoll.eps')
    fig.canvas.mpl_connect('pick_event', onpick)


    #fig.canvas.mpl_connect('pick_event', onpick())
    plt.show()




