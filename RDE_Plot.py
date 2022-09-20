
import matplotlib.pyplot as plt
import numpy as np

class RDE_Plotter:

    def __init__(self):


        pass

    def __repr__(self):

        pass

    def plot_raw_data(self, raw_data):

        data = raw_data
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        col = ax1.scatter(data['Time'], data['Current [nA]'],picker=True)
        # fig.savefig('pscoll.eps')
        fig.canvas.mpl_connect('pick_event', onpick3)

        show()
        fig.canvas.mpl_connect('pick_event', onpick3)
        plt.show()

    def onpick(self,event):
        ind = event.ind

        print('onpick3 scatter:', ind, npy.take(x, ind), npy.take(y, ind))




